import signal

def _handle_sigterm(_signal_number, _stack_frame):
	sys.exit(0)

signal.signal(signal.SIGTERM, _handle_sigterm)