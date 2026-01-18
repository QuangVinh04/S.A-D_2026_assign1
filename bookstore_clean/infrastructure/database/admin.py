from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CustomerModel, 
    BookModel, 
    CartModel, 
    CartItemModel
)


@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customer"""
    list_display = ('id', 'name', 'email', 'password_display')
    list_display_links = ('name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('email',)
    readonly_fields = ('password_display',)
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'email')
        }),
        ('Mật khẩu', {
            'fields': ('password', 'password_display'),
            'description': 'Mật khẩu đã được hash. Không thể xem được password gốc.'
        }),
    )
    
    def password_display(self, obj):
        """Hiển thị thông tin về password"""
        if obj.password:
            return format_html(
                '<span style="color: green;">✓ Mật khẩu đã được hash</span>'
            )
        return "Chưa có mật khẩu"
    password_display.short_description = 'Mật khẩu'
    
    def save_model(self, request, obj, form, change):
        """Override save để hash password khi tạo mới"""
        if not change:  # Nếu là tạo mới
            if 'password' in form.changed_data:
                password = form.cleaned_data.get('password')
                if password:
                    obj.set_password(password)
        elif 'password' in form.changed_data:  # Nếu là update và password thay đổi
            password = form.cleaned_data.get('password')
            if password:
                obj.set_password(password)
        super().save_model(request, obj, form, change)


@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book"""
    list_display = ('id', 'title', 'author', 'price_display', 'stock', 'is_available_display')
    list_display_links = ('title',)
    search_fields = ('title', 'author')
    list_filter = ('author',)
    ordering = ('title',)
    
    fieldsets = (
        ('Thông tin sách', {
            'fields': ('title', 'author')
        }),
        ('Giá và tồn kho', {
            'fields': ('price', 'stock'),
            'description': 'Giá sách và số lượng tồn kho'
        }),
    )
    
    def price_display(self, obj):
        """Hiển thị giá với định dạng đẹp"""
        return f"${obj.price:,.2f}" if obj.price else "$0.00"
    price_display.short_description = 'Giá'
    price_display.admin_order_field = 'price'
    
    def is_available_display(self, obj):
        """Hiển thị trạng thái có sẵn"""
        if obj.stock > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Có sẵn ({})</span>',
                obj.stock
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Hết hàng</span>'
            )
    is_available_display.short_description = 'Tồn kho'
    is_available_display.admin_order_field = 'stock'
    
    actions = ['make_in_stock', 'make_out_of_stock']
    
    def make_in_stock(self, request, queryset):
        """Action: Đặt stock = 10 cho các sách đã chọn"""
        updated = queryset.update(stock=10)
        self.message_user(request, f'{updated} sách đã được cập nhật stock = 10.')
    make_in_stock.short_description = "Đặt stock = 10"
    
    def make_out_of_stock(self, request, queryset):
        """Action: Đặt stock = 0 cho các sách đã chọn"""
        updated = queryset.update(stock=0)
        self.message_user(request, f'{updated} sách đã hết hàng.')
    make_out_of_stock.short_description = "Đặt hết hàng (stock = 0)"


class CartItemInline(admin.TabularInline):
    """Inline admin for CartItem trong Cart"""
    model = CartItemModel
    extra = 1
    readonly_fields = ('subtotal_display',)
    fields = ('book', 'quantity', 'subtotal_display')
    
    def subtotal_display(self, obj):
        """Hiển thị tổng tiền của item"""
        if obj.pk and obj.book:
            subtotal = obj.book.price * obj.quantity
            return f"${subtotal:,.2f}"
        return "-"
    subtotal_display.short_description = 'Tổng tiền'


# ... existing code ...

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart"""
    list_display = ('id', 'customer_name', 'customer_email', 'item_count', 'total_display', 'created_at')
    list_display_links = ('id',)
    search_fields = ('customer__name', 'customer__email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'total_display')
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Thông tin giỏ hàng', {
            'fields': ('customer',)
        }),
        ('Thời gian', {
            'fields': ('created_at',)
        }),
        ('Tổng tiền', {
            'fields': ('total_display',),
            'classes': ('collapse',)
        }),
    )
    
    def customer_name(self, obj):
        """Hiển thị tên khách hàng"""
        return obj.customer.name if obj.customer else "-"
    customer_name.short_description = 'Khách hàng'
    customer_name.admin_order_field = 'customer__name'
    
    def customer_email(self, obj):
        """Hiển thị email khách hàng"""
        return obj.customer.email if obj.customer else "-"
    customer_email.short_description = 'Email'
    customer_email.admin_order_field = 'customer__email'
    
    def item_count(self, obj):
        """Đếm số lượng items trong cart"""
        count = obj.items.count()
        return count
    item_count.short_description = 'Số lượng items'
    
    def total_display(self, obj):
        """Hiển thị tổng tiền của cart"""
        total = sum(
            item.book.price * item.quantity 
            for item in obj.items.all() 
            if item.book
        )
        # Format số trước, sau đó mới truyền vào format_html
        total_formatted = f"{total:,.2f}"
        return format_html(
            '<span style="font-size: 16px; font-weight: bold; color: green;">${}</span>',
            total_formatted
        )
    total_display.short_description = 'Tổng tiền'


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for CartItem"""
    list_display = ('id', 'cart_id', 'book_title', 'quantity', 'price_display', 'subtotal_display')
    list_display_links = ('id',)
    search_fields = ('book__title', 'cart__customer__name')
    list_filter = ('quantity',)
    readonly_fields = ('price_display', 'subtotal_display')
    
    fieldsets = (
        ('Thông tin', {
            'fields': ('cart', 'book')
        }),
        ('Số lượng và giá', {
            'fields': ('quantity', 'price_display', 'subtotal_display')
        }),
    )
    
    def cart_id(self, obj):
        """Hiển thị ID của cart"""
        return obj.cart.id if obj.cart else "-"
    cart_id.short_description = 'Cart ID'
    cart_id.admin_order_field = 'cart__id'
    
    def book_title(self, obj):
        """Hiển thị tên sách"""
        return obj.book.title if obj.book else "-"
    book_title.short_description = 'Sách'
    book_title.admin_order_field = 'book__title'
    
    def price_display(self, obj):
        """Hiển thị giá sách"""
        if obj.book:
            return f"${obj.book.price:,.2f}"
        return "-"
    price_display.short_description = 'Giá sách'
    
    def subtotal_display(self, obj):
        """Hiển thị tổng tiền"""
        if obj.book:
            subtotal = obj.book.price * obj.quantity
            # Format số trước, sau đó mới truyền vào format_html
            subtotal_formatted = f"{subtotal:,.2f}"
            return format_html(
                '<span style="font-weight: bold;">${}</span>',
                subtotal_formatted
            )
        return "-"
    subtotal_display.short_description = 'Tổng tiền'