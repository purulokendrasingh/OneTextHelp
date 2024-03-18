import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface DialogData {
  newPost: boolean;
}

@Component({
  selector: 'awaaz-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent {
  isNewPost = false;
  form: FormGroup;

  constructor(
    public dialogRef: MatDialogRef<DialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    public fb: FormBuilder
  ) {
    this.isNewPost = data.newPost;
    this.form = this.fb.group({
        name: ['', Validators.required],
        phone: ['', Validators.required],
        message: ['', Validators.required]
      });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

}
