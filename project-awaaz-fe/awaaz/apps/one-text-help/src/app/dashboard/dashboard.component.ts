import { Component, OnInit } from '@angular/core';
import { faFacebook, faTwitter } from '@fortawesome/free-brands-svg-icons';

import { CosmosService } from '../cosmos.service';
import { DatePipe } from '@angular/common';
import { DialogComponent } from '../dialog/dialog.component';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { SignalRService } from '../signalr.service';

@Component({
  selector: 'awaaz-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  posts: any[] = [];
  apiFailed = false;
  fbIcon = faFacebook;
  tweetIcon = faTwitter;
  datePipe = new DatePipe('en-US');

  constructor(
    public dialog: MatDialog,
    public signalRService: SignalRService,
    public cosmosService: CosmosService,
    public httpClient: HttpClient
  ) {}

  ngOnInit() {
    this.cosmosService.getProjects().then(
      (ps: any[]) => {
        ps.map((x) => {
          return {
            name: x.name,
            phone: x.phone,
            message: x.message,
            TweetId: x.TweetId,
          };
        }).forEach((post) => {
          this.posts.unshift(post);
        });
      },
      (err) => {
        console.log(err);
        this.apiFailed = true;
      }
    );
    this.signalRService.startConnection();
    this.signalRService.addTransferChartDataListener();
    this.signalRService.data.subscribe({
      next: (post) => {
        this.posts.unshift(post);
      },
      error: (err) => {
        this.apiFailed = true;
        console.log(err);
      },
    });
  }

  openInfoDialog(): void {
    this.dialog.open(DialogComponent, {
      width: '500px',
      data: { newPost: false },
    });
  }

  openNewPostDialog(): void {
    const dialogRef = this.dialog.open(DialogComponent, {
      width: '500px',
      data: { newPost: true },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        const payload = {
          ...result,
          datetime: this.datePipe.transform(new Date(), 'YYYY-MM-dd HH:MM:SS'),
        };
        const url =
          'https://ash-awaaz.azurewebsites.net:443/api/as-trail1/triggers/manual/invoke?api-version=2020-05-01-preview&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=z3RnbAhRfHYaJ9-6pdUZDkRAMZU9kBX4M5RzIMbosoM';
        this.httpClient.post<any>(url, payload).subscribe({
          next: (x) => {
            console.log(x);
          },
          error: (err) => {
            this.apiFailed = true;
            console.log(err);
          },
        });
      }
    });
  }
}
