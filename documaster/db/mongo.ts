import { MongoClient, Db, Collection, Document } from 'mongodb';
import { logger } from '../util/logger.js';

class MongoDB {
   private static instance: MongoDB;
   private client: MongoClient;
   private db!: Db;
   
   private constructor() {
       const uri = process.env.MONGO_URI || 'mongodb://localhost:27017';
       this.client = new MongoClient(uri);
       logger.put('[MongoDB] Instance created');
   }

   static getInstance(): MongoDB {
       if (!MongoDB.instance) {
           MongoDB.instance = new MongoDB();
       }
       return MongoDB.instance;
   }

   async connect(): Promise<void> {
       try {
           logger.put('[MongoDB] Connecting...');
           await this.client.connect();
           this.db = this.client.db(process.env.DB_NAME || 'loresmaster');
           logger.put(`[MongoDB] Connected to ${this.db.databaseName}`);
       } catch (error) {
           logger.put(`[MongoDB][Error] Connection failed: ${(error as Error).message}`);
           throw error;
       }
   }

   getCollection<T extends Document>(name: string): Collection<T> {
       if (!this.db) throw new Error('Database not connected');
       logger.put(`[MongoDB] Accessing collection: ${name}`);
       return this.db.collection<T>(name);
   }

   async close(): Promise<void> {
       try {
           await this.client.close();
           logger.put('[MongoDB] Connection closed');
       } catch (error) {
           logger.put(`[MongoDB][Error] Close failed: ${(error as Error).message}`);
           throw error;
       }
   }
}

export const mongodb = MongoDB.getInstance();