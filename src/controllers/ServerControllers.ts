import socketIo from 'socket.io-client';
import { Observable } from 'rxjs';

let SERVER_URL = 'http://localhost:5000';

export class SocketService {
    private socket!: SocketIOClient.Socket;

    public constructor() {
        //SERVER_URL = window.location.hostname + ":5000";
        //SERVER_URL = "34.70.217.218:5000"; //HORRIBLE hacky solution
        this.socket = socketIo(SERVER_URL);
    }

    public kill() {
        this.socket.disconnect();
    }

    public sendWithoutMessage(type: string): void {
        this.socket.emit(type);
    }

    public send(type: string, message: any): void {
        this.socket.emit(type, ...message);
    }

    public onEvent(event: string): Observable<any> {
        return new Observable<any>(observer => {
            this.socket.on(event, (data: any) => observer.next(data));
        });
    }
}

export default class Server {
    private static socketService: SocketService;

    public static init(): void {
        Server.socketService = new SocketService();
    }

    public static get(): SocketService {
        return Server.socketService
    }
}