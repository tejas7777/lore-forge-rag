import { IncomingMessage } from "http";
import formidable, {errors as formidableErrors} from 'formidable';
import { logger } from "./logger.js";
import fs from 'fs/promises';


export const parseMultiPartFile = async(req: IncomingMessage)=>{

    const form = formidable({
        keepExtensions: false,
        maxFileSize: 10 * 1024 * 1024, //Replace with a config 
        multiples: false,
    })

    const [fields, files] = await form.parse(req);

    const file = files.file?.[0];

    if (!file) {
        throw new Error('No file uploaded');
    }

    const content = await fs.readFile(file.filepath);

    return content;

}