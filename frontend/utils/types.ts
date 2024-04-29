export interface Anime {
    title: string;
    description: string;
    rating: number;
    id: number;
    createdAt: string;
}

export interface User {
    id: number;
    username: string;
    createdAt: string;
}

export interface Genre {
    id: number;
    name: string;
    createdAt: string;
}