__author__ = 'Bagman'
import colorsys


def hsv2rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def make_style(values, name_param, breaks=5):
    with open('body') as file:
        style = "\n".join([line.strip() for line in file])
    with open('rule_template') as file:
        rule = "\n".join([line.strip() for line in file])

    values = sorted(values)
    break_len = len(values) / breaks
    rules = []
    h = 1.28
    s = 0.97
    v = 0.90
    v_l = 0.10
    step = (v - v_l) / breaks

    for i in range(1, breaks):
        rules.append(rule.format(name='b{}'.format(i),
                                 title='b{}'.format(i),
                                 param=name_param,
                                 breaks=i*break_len,
                                 color="#{0:02x}{1:02x}{2:02x}".format(
                                     *hsv2rgb(h, s, v - i*step))))

    return style.format('\n'.join(rules))
