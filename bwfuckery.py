import sys

def main(argv, stdin):
	first_tape = [0]
	second_tape = [0]
	code = argv[1]
	tapes = "-t" in argv[2:]
	debug = "-d" in argv[2:]
	numeric = "-n" in argv[2:]
	tape_head = 0
	code_index = 0
	loop_depth = 0
	input_index = 0
	
	while code_index < len(code):
		char = code[code_index]
		if char == "^":
			first_tape[tape_head] ^= second_tape[tape_head]
		if char == "&":
			first_tape[tape_head] &= second_tape[tape_head]
		if char == "|":
			first_tape[tape_head] |= second_tape[tape_head]
		if char == "~":
			first_tape[tape_head] = ~first_tape[tape_head]
		if char == "@":
			first_tape, second_tape = second_tape, first_tape
		if char == "%":
			first_tape[tape_head], second_tape[tape_head] = second_tape[tape_head], first_tape[tape_head]
		if char == '{':
			first_tape[tape_head] <<= second_tape[tape_head]
		if char == '}':
			first_tape[tape_head] >>= second_tape[tape_head]

		if char == "+":
			first_tape[tape_head] += 1
		if char == "-":
			first_tape[tape_head] -= 1
		if char == ">":
			tape_head += 1
			try: first_tape[tape_head]
			except:
				first_tape.append(0)
				second_tape.append(0)
		if char == "<":
			tape_head -= 1
			if tape_head < 0:
				tape_head %= len(first_tape)
		if char == ".":
			if numeric: func = str
			else: func = chr
			print(end=func(abs(int(first_tape[tape_head]))))
		if char == ",":
			first_tape[tape_head] = ord(stdin[input_index]) if input_index < len(stdin) else -1
			input_index += 1

			
			
		if char == "[":
			loop_depth += 1
			if not first_tape[tape_head]:
				search = 1
				while search:
					code_index += 1
					if code[code_index] == '[': search += 1
					if code[code_index] == ']': search -= 1
				
		if char == "]":
			if first_tape[tape_head]:
				search = 1
				while search:
					code_index -= 1
					if code[code_index] == ']': search += 1
					if code[code_index] == '[': search -= 1
			else:
				loop_depth -= 1
				
		if char == "(":
			loop_depth += 1
			if (not first_tape[tape_head]&1):
				search = 1
				while search:
					code_index += 1
					if code[code_index] == '(': search += 1
					if code[code_index] == ')': search -= 1
		if char == ")":
			if (first_tape[tape_head]&1):
				search = 1
				while search:
					code_index -= 1
					if code[code_index] == ')': search += 1
					if code[code_index] == '(': search -= 1
			else:
				loop_depth -= 1
		code_index += 1

		if debug:
			print(char, code_index, tape_head, first_tape, second_tape, first_tape[tape_head]&1, file = sys.stderr)

	if tapes:
		while first_tape and first_tape[-1] == 0: first_tape.pop()
		while second_tape and second_tape[-1] == 0: second_tape.pop()
		print(first_tape, file = sys.stderr)
		print(second_tape, file = sys.stderr)

if __name__ == '__main__':
	main(sys.argv, sys.stdin.read())
