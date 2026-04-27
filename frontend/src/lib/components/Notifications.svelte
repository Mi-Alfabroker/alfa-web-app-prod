<script lang="ts">
	import { notifications, removeNotification, type NotificationType } from '$lib/stores/notifications';
	import { fly } from 'svelte/transition';

	const iconMap: Record<NotificationType, string> = {
		success: '✅',
		error: '❌',
		warning: '⚠️',
		info: 'ℹ️'
	};

	const bgColorMap: Record<NotificationType, string> = {
		success: 'bg-green-50 border-green-200 text-green-800',
		error: 'bg-red-50 border-red-200 text-red-800',
		warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
		info: 'bg-blue-50 border-blue-200 text-blue-800'
	};
</script>

<div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
	{#each $notifications as notification (notification.id)}
		<div
			class="flex items-center gap-3 p-4 rounded-lg border shadow-lg {bgColorMap[notification.type]}"
			transition:fly={{ x: 100, duration: 300 }}
		>
			<span class="text-xl">{iconMap[notification.type]}</span>
			<p class="flex-1 text-sm font-medium">{notification.message}</p>
			<button
				class="text-current opacity-50 hover:opacity-100 transition-opacity"
				on:click={() => removeNotification(notification.id)}
			>
				✕
			</button>
		</div>
	{/each}
</div>
