def customer_context(request):
    customer_id = request.session.get('customer_id')
    customer_name = request.session.get('customer_name')
    return {
        'customer_id': customer_id,
        'customer_name': customer_name,
        'is_customer_logged_in': customer_id is not None,
    }