import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})


export class DataService {

  constructor(private http: HttpClient) { }

  getUsers() {
    return this.http.get('/assets/contacts/contacts.json');
  }

  getEvents() {
    return this.http.get('/assets/events.json');
  }

}
