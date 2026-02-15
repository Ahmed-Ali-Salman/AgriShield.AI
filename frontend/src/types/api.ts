export interface ApiError {
    detail: string;
    code?: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    skip: number;
    limit: number;
}
