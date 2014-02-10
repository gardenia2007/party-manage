
pre_fix = 'controllers.'

urls = (
    "/",      					pre_fix + "index.Index",
    "/login", 					pre_fix + "index.Login",
    "/logout", 					pre_fix + "index.Logout",
    "/test",                    pre_fix + "index.Test",

    "/admin",					pre_fix + "admin.Index",
    "/admin/upload",            pre_fix + "admin.Upload",
    "/admin/add/student",       pre_fix + "admin.AddStudent",
    "/admin/add/teacher",       pre_fix + "admin.AddTeacher",
    "/admin/del/teacher/(\d+)", pre_fix + "admin.DelTeacher",
    "/admin/teacher/info/(\d+)",pre_fix + "admin.UpdateTeacherInfo",
    "/admin/status/student",    pre_fix + "admin.StatusStudent",
    "/admin/status/teacher",    pre_fix + "admin.StatusTeacher",
    "/admin/info/student",      pre_fix + "admin.InfoStudent",
    "/admin/info/teacher",      pre_fix + "admin.InfoTeacher",
    "/admin/manage/teacher",    pre_fix + "admin.ManageTeacher",

    "/student",                 pre_fix + "student.Index",
    "/student/teacher/my",      pre_fix + "student.TeacherMy",
    "/student/teacher/all",     pre_fix + "student.TeacherAll",
    "/student/teacher/info/(\d+)",pre_fix + "student.TeacherInfo",
    "/student/info",            pre_fix + "student.Info",
    "/student/choose/(\d+)",    pre_fix + "student.Choose",
    "/student/delete/(\d+)",    pre_fix + "student.Delete",

    "/teacher",                 pre_fix + "teacher.Index",
    "/teacher/student/my",      pre_fix + "teacher.StudentMy",
    "/teacher/student/info/(\d+)",pre_fix + "teacher.StudentInfo",
    "/teacher/info",            pre_fix + "teacher.Info",
    "/teacher/pass/(\d+)",      pre_fix + "teacher.Pass",
    "/teacher/fail/(\d+)",      pre_fix + "teacher.Fail",


    "/user",                    pre_fix + "user.Index",
    "/user/password",           pre_fix + "user.UpdatePw",
)

