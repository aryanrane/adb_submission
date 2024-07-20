import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTodos = () => apiClient.get('/todos/');
export const createTodo = (todo) => apiClient.post('/todos/', todo);
