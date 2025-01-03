import { IncomingMessage, ServerResponse } from "http";
import * as coreController from '../controller/core.js'

export const coreRouter = async (req: IncomingMessage, res: ServerResponse)=>{
    try{
        if (req.method === 'GET' && req.url === '/health') {
            const response = await coreController.healthCheck()
            res.end(JSON.stringify(response))
        } else if (req.method === 'POST' && req.url === '/ingest') {

            await coreController.ingestFile(req);
            
            res.statusCode = 200;
            res.end(JSON.stringify({ status: 'success', message: 'File received' }));
        } else {
            res.statusCode = 404;
            res.end(JSON.stringify({ status: 404, message: 'Route Not found' }));
        }
    } catch(error){

        console.log("[coreRouter][error]: "+error)

    }
}