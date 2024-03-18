import * as signalR from"@microsoft/signalr";

import { Injectable } from '@angular/core';
import { Subject } from "rxjs";

@Injectable({
  providedIn: 'root',
})
export class SignalRService {
  data: Subject<any> = new Subject<any>();
  hubConnection!: signalR.HubConnection;
  public startConnection = () => {
    this.hubConnection = new signalR.HubConnectionBuilder()
      .withUrl('http://localhost:7071/api/')
      .build();
    this.hubConnection
      .start()
      .then(() => console.log('Connection started'))
      .catch((err) => console.log('Error while starting connection: ' + err));
  };
  public addTransferChartDataListener = () => {
    this.hubConnection.on('target', (data) => {
      this.data.next(data);
      console.log(data);
    });
  };
}
