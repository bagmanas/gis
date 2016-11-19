__author__ = 'Bagman'
import colorsys

def hsv2rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def make_rule_less(name, title, name_param, color, breaks_left=0):
    with open('./style_generator/rule_less') as file:
        rule = "\n".join([line.strip() for line in file])

    return rule.format(name=name,
                       title=title,
                       param=name_param,
                       breaks=breaks_left,
                       color=color)


def make_rule_interval(name, title, name_param, color, breaks_left, breaks_right):
    with open('./style_generator/rule_interval') as file:
        rule = "\n".join([line.strip() for line in file])

    return rule.format(name=name,
                       title=title,
                       param=name_param,
                       breaks_left=breaks_left,
                       breaks_right=breaks_right,
                       color=color)


def make_rule_greater(name, title, name_param, color, breaks_right):
    with open('./style_generator/rule_greater') as file:
        rule = "\n".join([line.strip() for line in file])

    return rule.format(name=name,
                       title=title,
                       param=name_param,
                       breaks=breaks_right,
                       color=color)


def make_style(values, name_param, breaks=5):
    with open('./style_generator/body') as file:
        style = "\n".join([line.strip() for line in file])

    values = sorted(values)
    break_len = len(values) // breaks
    rules = []
    h = 1.28
    s = 0.97
    v = 0.90
    v_l = 0.10
    step = (v - v_l) / breaks

    prev = None
    for i in range(1, breaks):
        params = ['b{}'.format(i),
                  'b{}'.format(i),
                  name_param,
                  '#{0:02x}{1:02x}{2:02x}'.format(*hsv2rgb(h, s, v - i * step))]

        if i == 1:
            rule = make_rule_less(*(params + [values[i * break_len]]))
        elif i == breaks - 1:
            rule = make_rule_greater(*(params + [prev]))
        else:
            rule = make_rule_interval(*(params + [prev] + [values[i * break_len]]))
        prev = values[i * break_len]
        rules.append(rule)
    return style.format('\n'.join(rules))
