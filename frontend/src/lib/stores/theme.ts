import {
    writable
} from 'svelte/store';

type Theme='light' | 'dark';

export const theme=writable<Theme>('light');

theme.subscribe((value)=> {
    if (typeof document !=='undefined') {
        document.documentElement.dataset.theme=value;
    }
});