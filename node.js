const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const app = express();
const port = process.env.PORT || 3000;

// Middleware for parsing JSON and URL-encoded data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Endpoint for chatbot interaction
app.post('/chat', (req, res) => {
    const userInput = req.body.message;
    const pythonProcess = spawn('python', ['./node.py']); // Adjust path if necessary

    pythonProcess.stdin.write(JSON.stringify({ message: userInput }));
    pythonProcess.stdin.end();

    let dataToSend = '';

    pythonProcess.stdout.on('data', function(data) {
        dataToSend += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send({ error: 'Python script failed' });
        }
        res.json(JSON.parse(dataToSend));
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});