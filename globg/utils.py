import decimal

# N u m e r i c   F u n c t i o n s

def round_half_up(value, digits):
    # 1.155 = 1.16, 1.154 = 1.15
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    return float( round(decimal.Decimal(value), digits) )

def round_half_up_decimal(value, digits):
    # 1.155 = 1.16, 1.154 = 1.15
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    return round(decimal.Decimal(value), digits)

def currency_value(value, coin_symbol):
    return '{:,.2f} {}'.format(value, coin_symbol)

def str_to_float_or_zero(str_value):
    try:
        return float(str_value)
    except:
        return 0.0

def str_to_int_or_zero(str_value):
    try:
        return int(str_value)
    except:
        return 0