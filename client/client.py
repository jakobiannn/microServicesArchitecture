import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8000")

print('Ping:', server.ping())
print('Server datetime:', server.now())
print('View, operation_type, value:', server.operation_type(2))
print('View, operation_type, value:', server.operation_type(2.))
print('View, operation_type, value:', server.operation_type('My string'))
print('View, operation_type, value:', server.operation_type("My string"))
print('View, operation_type, value:', server.operation_type([1, 2, 3]))
print('View, operation_type, value:', server.operation_type(["one", "two", "three"]))
print('View, operation_type, value:', server.operation_type((1, 2, "3")))
print('Sum 2 + 3 :', server.sum(2, 3))
print('Pow 2^3: ', server.pow(2, 3))

print('Get logs by date: ')
for x in server.get_stats_by_date('2022-12-10 16:32:26', '2022-12-10 16:33:15'): print(x)

print('Get logs by operation_type: ')
for x in server.get_stats_by_type('operation_type'): print(x)

print('Get logs by duration: ')
for x in server.get_stats_by_duration(0.0000000000001, 0.000001907349): print(x)
