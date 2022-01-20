file = open('urls.txt','a+',encoding='utf-8')
words = input("Enter the Words: ")
domains = input("Enter the domains: ")

domain = domains.split()

for i in domain:
 url = 'site:.' + i  + ' (' + words + ')'
 file.write(url + '\n')