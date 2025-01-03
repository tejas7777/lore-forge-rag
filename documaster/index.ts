import http from 'http';
import { IncomingMessage, ServerResponse } from 'http';
import { coreRouter } from './routes/core.js';
import { mongodb } from './db/mongo.js';
import { rabbitmq } from './services/rabbitmq.js';

const startServer = async () => {
   try {
       await mongodb.connect();
       await rabbitmq.connect();
       
       const server = http.createServer(
           async (req: IncomingMessage, res: ServerResponse) => {
               res.setHeader('Content-Type', 'application/json');
               await coreRouter(req,res);
           }
       );

       const port = process.env.SERVER_POST || 5001;
       server.listen(port, () => {
            const devURL = `http://localhost:${port}`
            console.log(`Server running on ${process.env.SERVER_URL || devURL}`);
       });
   } catch (error) {
       console.error('Failed to start:', error);
       process.exit(1);
   }
}

startServer();