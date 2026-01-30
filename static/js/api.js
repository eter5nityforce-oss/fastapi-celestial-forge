class API {
    constructor() {
        this.baseUrl = "";
        this.token = localStorage.getItem("token");
    }

    async login(username, password) {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${this.baseUrl}/token`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const data = await response.json();
        this.token = data.access_token;
        localStorage.setItem("token", this.token);
        localStorage.setItem("username", username);
        return data;
    }

    async register(username, password) {
        const response = await fetch(`${this.baseUrl}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Registration failed");
        }
        return await response.json();
    }

    async createGame() {
        const response = await fetch(`${this.baseUrl}/game/create`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${this.token}` }
        });

        if (!response.ok) {
            throw new Error("Failed to create game");
        }
        return await response.json();
    }
}

const api = new API();
