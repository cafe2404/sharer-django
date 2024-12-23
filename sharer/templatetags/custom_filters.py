from django import template
import locale
from decimal import Decimal

register = template.Library()

@register.filter
def parse_currency(value):
    """
    Chuyển đổi số hoặc chuỗi thành định dạng tiền tệ VNĐ.
    """
    if not value:
        return value
    try:
        # Đặt locale cho tiền tệ Việt Nam
        locale.setlocale(locale.LC_ALL, 'vi_VN.utf8')
        # Chuyển giá trị thành Decimal nếu cần
        if isinstance(value, str):
            value = Decimal(value.replace(',', '').replace('đ', '').strip())
        # Định dạng thành tiền tệ
        formatted_value = locale.format_string('%.0f', value, grouping=True)
        return f"{formatted_value} ₫"
    except Exception as e:
        return f"Error: {str(e)}"

@register.filter
def obscure_email(value):
    if '@' in value:
        local, domain = value.split('@')
        if len(local) > 2:
            local = local[0] + '*' * (len(local) - 2) + local[-1]
        domain_parts = domain.split('.')
        domain_parts[0] = '*' * len(domain_parts[0])
        return f"{local}@{'.'.join(domain_parts)}"
    return value

@register.filter
def slice(value, arg):
    if not value:
        return value
    start, end = map(int, arg.split(','))
    return value[start:end]