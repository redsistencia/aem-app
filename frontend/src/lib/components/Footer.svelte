<footer class="footer">
	<div class="container">
		<p>© {new Date().getFullYear()} Argentinxs en Mallorca</p>

		<ul class="links">
			<li><a href="/privacidad">Privacidad</a></li>
			<li><a href="/baja">Darse de baja</a></li>
			<li><a href="mailto:redsistencia.baleares@gmail.com">Contacto</a></li>
		</ul>
	</div>
</footer>

<style>
	.footer {
		background-color: var(--color-bg-muted);
		border-top: 1px solid var(--color-border);
		margin-top: var(--space-xl);
	}

	.container {
		max-width: 1024px;
		margin: 0 auto;
		padding: var(--space-lg) var(--space-md);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
	}

	p {
		color: var(--color-text-muted);
		font-size: 0.875rem;
	}

	.links {
		display: flex;
		gap: var(--space-md);
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.links a {
		color: var(--color-text-muted);
		font-size: 0.875rem;
	}
</style>
