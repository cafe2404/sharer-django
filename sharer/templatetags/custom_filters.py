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
