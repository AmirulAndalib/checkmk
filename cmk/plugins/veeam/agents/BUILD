exports_files(
    ["veeam_backup_status.ps1"],
    visibility = ["//agents/windows/plugins:__pkg__"],
)

filegroup(
    name = "powershell_scripts",
    srcs = ["veeam_backup_status.ps1"],
    tags = ["lint-with-psscriptanalyzer"],
)
