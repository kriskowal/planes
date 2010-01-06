
# Run ./pyshd graph_demo.py
# and browse to https://localhost:2380
# pyshd requires system credentials
# requires AuthShadow, SSL, and pygraph

from planes.python.graphkit import *

q0 = Node('q0')
q1 = Node('q1')
q0.connect(q1)
q1.connect(q0)
g = Graph((q0, q1))

