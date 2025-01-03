import amqp, { Connection, Channel } from 'amqplib';
import { logger } from '../util/logger.js';

class RabbitMQ {
   private static instance: RabbitMQ;
   private connection!: Connection;
   private channel!: Channel;
   
   private constructor() {
       logger.put('[RabbitMQ] Instance created');
   }

   static getInstance(): RabbitMQ {
       if (!RabbitMQ.instance) {
           RabbitMQ.instance = new RabbitMQ();
       }
       return RabbitMQ.instance;
   }

   async connect(): Promise<void> {
       try {
           const url = process.env.RABBITMQ_URL || 'amqp://localhost';
           this.connection = await amqp.connect(url);
           this.channel = await this.connection.createChannel();
           logger.put('[RabbitMQ] Connected');
       } catch (error) {
           logger.put(`[RabbitMQ][Error] Connection failed: ${(error as Error).message}`);
           throw error;
       }
   }

   async publishMessage(queue: string, message: string): Promise<void> {
       await this.channel.assertQueue(queue);
       this.channel.sendToQueue(queue, Buffer.from(message));
       logger.put(`[RabbitMQ] Message sent to queue: ${queue}`);
   }

   async close(): Promise<void> {
       await this.channel?.close();
       await this.connection?.close();
       logger.put('[RabbitMQ] Connection closed');
   }
}

export const rabbitmq = RabbitMQ.getInstance();
