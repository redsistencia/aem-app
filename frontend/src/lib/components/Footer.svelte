<script lang="ts">
	import { Instagram } from 'lucide-svelte';
</script>

<footer class="border-t bg-muted/40">
	<div class="container mx-auto px-4 py-8 space-y-4">
		<p class="text-sm text-muted-foreground">
			© 2026 Redsistencia baleares
		</p>

		<ul class="flex flex-wrap items-center gap-4 text-sm">
			<li>
				<a
					href="/privacidad"
					class="text-muted-foreground hover:text-foreground transition-colors"
				>
					Privacidad
				</a>
			</li>

			<li>
				<a
					href="/baja"
					class="text-muted-foreground hover:text-foreground transition-colors"
				>
					Darse de baja
				</a>
			</li>

			<li class="flex items-center gap-3">
				<a
					href="mailto:redsistencia.baleares@gmail.com"
					class="text-muted-foreground hover:text-foreground transition-colors"
				>
					Contacto
				</a>

				<a
					href="https://www.instagram.com/redsistencia.baleares/"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="Instagram de Redsistencia"
					class="text-muted-foreground hover:text-foreground transition-colors"
				>
					<Instagram class="h-4 w-4" />
				</a>
			</li>
		</ul>
	</div>
</footer>
