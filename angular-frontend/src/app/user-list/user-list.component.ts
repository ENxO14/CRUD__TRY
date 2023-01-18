import { Observable } from "rxjs";
import { UserService } from "../user.service";
import { User } from "../user";
import { Component, OnInit } from "@angular/core";
import { Router } from '@angular/router';

@Component({
  selector: "app-user-list",
  templateUrl: "./user-list.component.html",
  styleUrls: ["./user-list.component.css"]
})
export class UserListComponent implements OnInit {
  data: User[] = undefined!;
  obsRooms: Observable<User[]> | undefined


  constructor(private userService: UserService, private router: Router) { }

  ngOnInit() {
    this.reloadData();
  }

  reloadData() {
    this.obsRooms = this.userService.getUsersList()
    this.obsRooms.subscribe(this.fati)
  }
  fati = (data: User[]) => {
    this.data = data;
  }


  deleteUser(id: string) {
    this.userService.deleteUser(id)
      .subscribe(
        data => {
          console.log(data);
          this.reloadData();
        },
        error => console.log(error));
  }
  updateUser(id: string) {
    this.router.navigate(['update', id]);
  }
}