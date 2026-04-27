/**
 * Notification store for toast messages
 */

import { writable } from 'svelte/store';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
	id: string;
	type: NotificationType;
	title?: string;
	message: string;
	duration?: number;
}

function createNotificationStore() {
	const { subscribe, update } = writable<Notification[]>([]);

	return {
		subscribe,
		add: (notification: Omit<Notification, 'id'>) => {
			const id = crypto.randomUUID();
			const newNotification = { ...notification, id };

			update((notifications) => [...notifications, newNotification]);

			// Auto-remove after duration (default 5 seconds)
			if (notification.duration !== 0) {
				setTimeout(() => {
					update((notifications) => notifications.filter((n) => n.id !== id));
				}, notification.duration || 5000);
			}

			return id;
		},
		remove: (id: string) => {
			update((notifications) => notifications.filter((n) => n.id !== id));
		},
		clear: () => {
			update(() => []);
		}
	};
}

export const notifications = createNotificationStore();

// Convenience functions
export const addNotification = notifications.add;
export const removeNotification = notifications.remove;
export const clearNotifications = notifications.clear;
