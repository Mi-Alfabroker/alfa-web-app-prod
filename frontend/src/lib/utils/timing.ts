/**
 * Timing utility functions
 */

/**
 * Debounce a function - delays execution until after wait milliseconds
 * have elapsed since the last time it was invoked
 */
export function debounce<T extends (...args: Parameters<T>) => ReturnType<T>>(
	func: T,
	wait: number
): (...args: Parameters<T>) => void {
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
		if (timeoutId) {
			clearTimeout(timeoutId);
		}
		timeoutId = setTimeout(() => {
			func.apply(this, args);
		}, wait);
	};
}

/**
 * Throttle a function - ensures it's only called at most once
 * in a specified time period
 */
export function throttle<T extends (...args: Parameters<T>) => ReturnType<T>>(
	func: T,
	limit: number
): (...args: Parameters<T>) => void {
	let inThrottle = false;

	return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
		if (!inThrottle) {
			func.apply(this, args);
			inThrottle = true;
			setTimeout(() => {
				inThrottle = false;
			}, limit);
		}
	};
}
