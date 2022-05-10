import mice
separator = ';'

for rule in mice.rules:
    for indicator in rule.indicators:
        res = indicator.result()
        value_set = 0
        for item in res:
            report = open(mice.result_path + '/' + item[2][0] + '.csv', 'w')
            headers = item[0]
            values = item[1]
            report.write(separator.join(headers) + '\n')
            colomn_num = len(values)
            if colomn_num:
                row_num = len(values[0])
            else:
                continue
            for row in range(row_num):
                row_str = []
                for value in values:
                    row_str.append(str(value[row]))
                report.write(separator.join(row_str) + '\n')
            value_set += 1
report.close()

#html mini report
report = open(mice.result_path + '/report.html', 'w')
report.write('<pre>\n')
for rule in mice.rules:
    for indicator in rule.indicators:
        res = indicator.result()
        for item in res:
            headers = item[0]
            values = item[1]
            for header, value in zip(headers, values):
                report.write("%(header)s %(value)s\n" % locals())
report.write('</pre>\n')