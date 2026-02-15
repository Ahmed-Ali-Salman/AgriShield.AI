export function isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function isValidPassword(password: string): boolean {
    return password.length >= 6;
}

export function isValidScore(value: number): boolean {
    return value >= 0 && value <= 100;
}
