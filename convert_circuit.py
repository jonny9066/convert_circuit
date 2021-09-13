
filename = 'aes_128.txt'

dst_filename = 'temp.py'

f = open(filename)


lines = iter(f)
next_line = lambda: next(lines).split()
n_gates, n_wires = (int(x) for x in next_line())
input_line = [int(x) for x in next_line()]
n_inputs = input_line[0]
n_input_wires = input_line[1:]
assert(n_inputs == len(n_input_wires))
output_line = [int(x) for x in next_line()]
n_outputs = output_line[0]
next(lines)


# out_circuit = []
# for i_wire in range(n_input_wires[0]):
#     out_circuit.append('w%d = sint.get_input_from(0)'%i_wire)
# for i_wire in range(n_input_wires[1]):
#     out_circuit.append('w%d = sint.get_input_from(1)'%(i_wire+128))

out_circuit = []
for i_wire in range(n_input_wires[0]):
    out_circuit.append('w%d = 0'%i_wire)
for i_wire in range(n_input_wires[1]):
    out_circuit.append('w%d = 0'%(i_wire+128))

st1 = 'print_ln(\''
# st2 = '\','
st2 = '\'%('

clen = 0
for i in range(n_gates):
    line = next_line()
    t = line[-1]
    if t in ('XOR', 'AND'):
        assert line[0] == '2'
        assert line[1] == '1'
        assert len(line) == 6
        if t == 'XOR':
            out_circuit.append('w%d = my_xor(w%d, w%d)'%(int(line[4]),int(line[2]), int(line[3])))
        else:
            out_circuit.append('w%d = my_and(w%d, w%d)'%(int(line[4]),int(line[2]), int(line[3])))
    elif t == 'INV':
        assert line[0] == '1'
        assert line[1] == '1'
        assert len(line) == 5
        out_circuit.append('w%d = my_inv(w%d)'%(int(line[-2]),int(line[-3])))
    if i >= n_gates-128:
        # wire = 'w'+line[-2]+'.reveal()'
        # st1 += '%s'
        # st2 += wire +', '
        st1 += '%d'
        st2+= 'w'+line[-2]+','
        clen+=1
assert(clen == 128)   
# st2 = st2[:-2] +')'
st2 = st2[:-1] +'))'
print_statement = st1+st2
out_circuit.append(print_statement)


f = open(dst_filename, 'w')
for l in out_circuit:
    f.write(l)
    f.write('\n')
