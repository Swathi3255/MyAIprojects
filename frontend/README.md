# AI Chat Assistant Frontend

A modern, responsive React frontend for the OpenAI Chat API built with FastAPI.

## Features

- 🤖 **Real-time Chat Interface** - Stream responses from OpenAI models
- 🎨 **Modern UI/UX** - Beautiful gradient design with smooth animations
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 🔧 **Model Selection** - Choose between GPT-4.1 Mini, GPT-4, and GPT-3.5 Turbo
- ⚙️ **Customizable System Messages** - Define the AI's behavior and role
- 🔒 **Secure API Key Input** - Password-protected API key field
- 💬 **Message History** - View conversation history with timestamps
- ⌨️ **Keyboard Shortcuts** - Press Enter to send, Shift+Enter for new line

## Prerequisites

- Node.js (version 16 or higher)
- npm or yarn
- Running FastAPI backend (see `/api` directory)

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and go to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm start` - Start the application

## Configuration

The frontend is configured to proxy API requests to `http://localhost:8000` (your FastAPI backend). This is set up in `vite.config.js`.

## Usage

1. **Get an OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key (it starts with `sk-`)

2. **Start the Backend**:
   ```bash
   cd ../api
   pip install -r requirements.txt
   python app.py
   ```

3. **Start the Frontend**:
   ```bash
   cd ../frontend
   npm run dev
   ```

4. **Use the Application**:
   - Enter your OpenAI API key
   - Optionally customize the system message
   - Select your preferred model
   - Type your message and press Enter or click Send

## API Integration

The frontend communicates with the FastAPI backend through the `/api/chat` endpoint:

- **POST** `/api/chat` - Send chat messages and receive streaming responses
- **GET** `/api/health` - Check API health status

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── App.jsx          # Main application component
│   ├── main.jsx         # Application entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
└── README.md           # This file
```

## Styling

The application uses modern CSS with:
- CSS Grid and Flexbox for layout
- CSS Custom Properties for theming
- Smooth animations and transitions
- Responsive design patterns
- Glassmorphism effects

## Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Ensure the FastAPI backend is running on port 8000
   - Check that CORS is properly configured in the backend

2. **Module Not Found**:
   - Run `npm install` to install dependencies
   - Check that you're in the correct directory

3. **Build Errors**:
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

### Development Tips

- Use browser developer tools to debug API calls
- Check the Network tab for request/response details
- Monitor console for any JavaScript errors

## Deployment

For production deployment:

1. Build the application:
   ```bash
   npm run build
   ```

2. The `dist` folder contains the production build

3. Deploy to your preferred hosting service (Vercel, Netlify, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AI Engineer Challenge.