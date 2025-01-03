import { IncomingMessage } from "http"
import { logger } from "../util/logger.js"
import { parseMultiPartFile } from "../util/fileUtil.js"
import { mongodb } from "../db/mongo.js"
import { rabbitmq } from "../services/rabbitmq.js"

type FileDoc = {
    content: Buffer;
    uploadedAt: Date;
 }

export const healthCheck = async (): Promise<TRespose> =>{
    try {
        return {
            statusCode: 200,
            message: 'success',
        }
        
    } catch (error) {
        logger.put("[healthCheck][error] "+(error as Error).message)
        return {
            statusCode: 500,
            message: 'Server Error',
        }
    }
}

export const ingestFile = async (req: IncomingMessage): Promise<TRespose> => {
    try {
        const fileData = await parseMultiPartFile(req);

        const uploadData = {
            content: fileData,
            uploadedAt: new Date()
        }
        
        const collection = mongodb.getCollection<FileDoc>('lorestore');
        const result = await collection.insertOne(uploadData);
 
        logger.put(`[controller][core][ingestFile][success] file saved`);

        await rabbitmq.publishMessage('rag_queue', result.insertedId.toString());
        
        logger.put(`[controller][core][ingestFile][success] id added on queue`);
 
        return {
            statusCode: 200,
            message: 'success',
        }
        
    } catch (error) {
        logger.put("[coreController][error] "+(error as Error).message);
        return {
            statusCode: 500,
            message: 'Server Error',
        }
    }
 }