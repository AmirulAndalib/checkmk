exports_files(
    ["nvidia_smi.ps1"],
    visibility = ["//agents/windows/plugins:__pkg__"],
)

filegroup(
    name = "powershell_scripts",
    srcs = ["nvidia_smi.ps1"],
    tags = ["lint-with-psscriptanalyzer"],
)
