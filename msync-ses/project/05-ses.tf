resource "aws_ses_template" "properline_email" {
  name    = "properline_email"
  subject = "Nowe konto pocztowe, {{username}}"
  html    =  file("${path.module}/code/msg.html")
}

