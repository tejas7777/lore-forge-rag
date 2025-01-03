class Logger {
    /*
    TODO: For now I am using the console.
    Will repace it with a proper logging service later on
    */

    private logger;

    constructor(){

    
        this.logger = console
    }

    put(logText: string){
        console.log(logText)
    }

}


export const logger = new Logger()