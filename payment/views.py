from django.shortcuts import render
import razorpay
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from wallet.models import Wallet, WalletTransaction
from plans.models import Plans
from wallet.serializers import WalletSerializer

from accounts.models import User, UserType
from rest_framework.permissions import IsAuthenticated
import hmac
import hashlib
from django.db import transaction

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# class CreateRazorpayOrderAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         amount = request.data.get('amount')
#         plan_id = request.data.get('plan_id')
#         number = request.data.get('number')

#         # Validate amount
#         try:
#             amount = Decimal(amount)
#             if amount <= 0:
#                 return Response({'error': 'Amount must be greater than 0'}, status=400)
#         except:
#             return Response({'error': 'Invalid amount'}, status=400)

#         # Validate plan
#         plan = get_object_or_404(Plans, pk=plan_id)

#         # Validate number (optional)
#         if not number or len(number) < 8:
#             return Response({'error': 'Invalid number'}, status=400)

#         amount_paise = int(amount * 100)

#         order = client.order.create({
#             "amount": amount_paise,
#             "currency": "INR",
#             "payment_capture": 1
#         })

#         return Response({
#             "order_id": order['id'],
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "amount": amount_paise,
#             "currency": "INR",
#             "plan_id": plan.id,
#             "number": number
#         }, status=200)

class CreateRazorpayOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        plan_id = request.data.get('plan_id')
        number = request.data.get('number')

        # Validate amount
        try:
            amount = Decimal(amount)
            if amount <= 0:
                return Response({'error': 'Amount must be greater than 0'}, status=400)
        except:
            return Response({'error': 'Invalid amount'}, status=400)

        # Validate plan
        plan = get_object_or_404(Plans, pk=plan_id)

        # Validate number
        if not number or len(number) < 8:
            return Response({'error': 'Invalid number'}, status=400)

        amount_paise = int(amount * 100)

        try:
            with transaction.atomic():
                # Create Razorpay order
                order = client.order.create({
                    "amount": amount_paise,
                    "currency": "INR",
                    "payment_capture": 1
                })

                # Get or create wallet
                wallet, _ = Wallet.objects.get_or_create(user=request.user)

                # Save a pending wallet transaction
                WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_type='add_to_wallet',
                    amount=amount,
                    description=f"Wallet top-up initiated via Razorpay for plan {plan.title}",
                    status='pending',
                    payment_id=order['id'],
                    created_by=request.user
                )

                return Response({
                    "order_id": order['id'],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "amount": amount_paise,
                    "currency": "INR",
                    "plan_id": plan.id,
                    "number": number,
                    "message": "Order created successfully. Awaiting payment."
                }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

# class RazorpayPaymentSuccessAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data
#         required_fields = [
#             'razorpay_order_id', 'razorpay_payment_id',
#             'razorpay_signature', 'amount',
#             'plan_id', 'number'
#         ]

#         if not all(field in data for field in required_fields):
#             return Response({'error': 'Missing required fields'}, status=400)

#         # Signature verify
#         generated_signature = hmac.new(
#             bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
#             bytes(f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}", 'utf-8'),
#             hashlib.sha256
#         ).hexdigest()

#         if generated_signature != data['razorpay_signature']:
#             return Response({'error': 'Invalid signature'}, status=400)

#         # Validate plan again
#         plan = get_object_or_404(Plans, pk=data['plan_id'])

#         # Validate number
#         number = data['number']

#         # Wallet debit-credit logic stays the same
#         client_user = request.user
#         admin_user = get_object_or_404(User, user_type=UserType.ADMIN)

#         amount = Decimal(data['amount'])

#         client_wallet = get_object_or_404(Wallet, user=client_user)
#         admin_wallet = get_object_or_404(Wallet, user=admin_user)

#         if not client_wallet.can_debit(amount):
#             return Response({'error': 'Insufficient balance'}, status=400)

#         client_wallet.debit_balance(amount)
#         WalletTransaction.objects.create(
#             wallet=client_wallet,
#             transaction_type='debit_from_wallet',
#             amount=amount,
#             description=f'Payment for plan {plan.title} to number {number}',
#             created_by=client_user
#         )

#         admin_wallet.add_balance(amount)
#         WalletTransaction.objects.create(
#             wallet=admin_wallet,
#             transaction_type='add_to_wallet',
#             amount=amount,
#             description=f'Received payment for plan {plan.title} from {client_user.email}',
#             created_by=client_user
#         )

#         # You may store the recharge record here if needed!

#         return Response({
#             'success': True,
#             'message': f'Payment verified. Plan {plan.title} will be recharged to {number}'
#         }, status=200)
class RazorpayPaymentSuccessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        required_fields = [
            'razorpay_order_id', 'razorpay_payment_id',
            'razorpay_signature', 'amount',
            'plan_id', 'number'
        ]

        # Check required fields
        if not all(field in data for field in required_fields):
            return Response({'error': 'Missing required fields'}, status=400)

        # Verify Razorpay signature
        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
            bytes(f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}", 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != data['razorpay_signature']:
            return Response({'error': 'Invalid signature'}, status=400)

        # Validate plan and number
        plan = get_object_or_404(Plans, pk=data['plan_id'])
        number = data['number']
        amount = Decimal(data['amount'])

        # Wallet logic
        client_user = request.user
        admin_user = get_object_or_404(User, user_type=UserType.ADMIN)

        client_wallet = get_object_or_404(Wallet, user=client_user)
        admin_wallet = get_object_or_404(Wallet, user=admin_user)

        if not client_wallet.can_debit(amount):
            return Response({'error': 'Insufficient balance'}, status=400)

        # Perform debit/credit transactions
        client_wallet.debit_balance(amount)
        WalletTransaction.objects.create(
            wallet=client_wallet,
            transaction_type='debit_from_wallet',
            amount=amount,
            description=f'Payment for plan {plan.title} to number {number}',
            created_by=client_user
        )

        admin_wallet.add_balance(amount)
        WalletTransaction.objects.create(
            wallet=admin_wallet,
            transaction_type='add_to_wallet',
            amount=amount,
            description=f'Received payment for plan {plan.title} from {client_user.email}',
            created_by=client_user
        )

        # You can create a RechargeRecord here if needed

        # 🔽 Frontend Friendly Response
        return Response({
            'success': True,
            'message': f'✅ Payment verified successfully. Recharge for plan **{plan.title}** will be applied to **{number}**.',
            'plan': {
                'id': plan.id,
                'title': plan.title,
                'description': plan.description,
                'amount': float(amount),
                'validity': plan.validity
            },
            'user': {
                'id': client_user.id,
                'email': client_user.email
            },
            'wallet': {
                'balance': float(client_wallet.balance),
                'debited': float(amount)
            },
            'razorpay': {
                'order_id': data['razorpay_order_id'],
                'payment_id': data['razorpay_payment_id']
            }
        }, status=200)
# class CreateRazorpayOrderAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         amount = request.data.get('amount')

#         try:
#             amount = Decimal(amount)
#             if amount <= 0:
#                 return Response({'error': 'Amount must be greater than 0'}, status=400)
#         except:
#             return Response({'error': 'Invalid amount'}, status=400)

#         amount_paise = int(amount * 100)

#         order = client.order.create({
#             "amount": amount_paise,
#             "currency": "INR",
#             "payment_capture": 1
#         })

#         return Response({
#             "order_id": order['id'],
#             "razorpay_key": settings.RAZORPAY_KEY_ID,
#             "amount": amount_paise,
#             "currency": "INR"
#         }, status=200)


# class RazorpayPaymentSuccessAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data
#         required_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount']

#         if not all(field in data for field in required_fields):
#             return Response({'error': 'Missing required payment fields'}, status=400)

#         # Verify signature
#         generated_signature = hmac.new(
#             bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
#             bytes(f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}", 'utf-8'),
#             hashlib.sha256
#         ).hexdigest()

#         if generated_signature != data['razorpay_signature']:
#             return Response({'error': 'Invalid signature'}, status=400)

#         # Fetch users
#         client_user = request.user
#         admin_user = get_object_or_404(User, user_type=UserType.ADMIN)

#         amount = Decimal(data['amount'])

#         # Wallet operations
#         client_wallet = get_object_or_404(Wallet, user=client_user)
#         admin_wallet = get_object_or_404(Wallet, user=admin_user)

#         if not client_wallet.can_debit(amount):
#             return Response({'error': 'Insufficient balance in wallet'}, status=400)

#         # Debit client
#         client_wallet.debit_balance(amount)
#         WalletTransaction.objects.create(
#             wallet=client_wallet,
#             transaction_type='debit_from_wallet',
#             amount=amount,
#             description=f'Payment made to admin by {client_user.email}',
#             created_by=client_user
#         )

#         # Credit admin
#         admin_wallet.add_balance(amount)
#         WalletTransaction.objects.create(
#             wallet=admin_wallet,
#             transaction_type='add_to_wallet',
#             amount=amount,
#             description=f'Received payment from {client_user.email}',
#             created_by=client_user
#         )

#         return Response({'success': True, 'message': 'Payment verified and wallet updated'}, status=200)
