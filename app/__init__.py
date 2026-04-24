"""
Pacote `app` - inicialização do pacote.

Configura output para UTF-8 no Windows de forma segura
para evitar `UnicodeEncodeError` ao imprimir emojis na console.
"""
import sys
if sys.platform == 'win32':
	try:
		import io

		# Só reconfigura quando a stream tem 'buffer' e o buffer não está fechado.
		def safe_wrap(stream):
			buf = getattr(stream, 'buffer', None)
			if buf is None:
				return stream
			# Se o buffer já está fechado, não reconfigurar
			if getattr(buf, 'closed', False):
				return stream
			# Evita re-wrapping se já usa UTF-8
			enc = getattr(stream, 'encoding', '') or ''
			if enc.lower() == 'utf-8':
				return stream
			try:
				return io.TextIOWrapper(buf, encoding='utf-8', errors='replace', line_buffering=True)
			except Exception:
				return stream

		sys.stdout = safe_wrap(sys.stdout)
		sys.stderr = safe_wrap(sys.stderr)
	except Exception:
		# Se por algum motivo não for possível reconfigurar, continuar sem falhar
		pass
