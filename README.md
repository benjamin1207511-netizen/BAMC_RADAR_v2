# BAMC RADAR 2.0 — 双源雷达（以可验证的真实图像为先）

## 重要的诚实说明
本版本不再把两家完整网页放进 iframe 作为“雷达图”。它采用 GitHub Actions 在服务器端获取香港天文台官方 256 km 雷达 KML 索引，解析其中最新的 PNG 图片地址，并校验返回内容确实是 PNG，再将图像发布到 GitHub Pages 同源路径。

**香港源：** 使用公开的 HKO KML 索引：
`https://www.hko.gov.hk/wxinfo/radars/R4_GIS_rad_256/R4_GIS_server_Radar_256.kml`
脚本会验证 HTTP 响应、KML XML、图像 PNG 文件头；抓取失败会让 Action 明确失败，不会静默显示占位图。该 URL 是公开网页资料中记载的 HKO 雷达索引/图片机制，但首次部署后仍应运行工作流并检查日志，以确认当前实际可访问性。

**澳门源：** 目前没有在这个代码包中冒称已经接通。澳门页面可以访问，但当前尚未从可验证来源确认其雷达图片的直接 URL 或接口；本页会明确标为“接口待验证”。必须先在浏览器 DevTools Network 中确认该官方页面加载雷达时实际请求的图像/数据 URL，才能写出可靠抓取器。

## 目录结构
```text
BAMC_RADAR_v2/
├── index.html
├── README.md
├── scripts/
│   └── fetch_hko_radar.py
├── .github/
│   └── workflows/
│       └── update-radar.yml
└── site/
    └── data/
        └── .gitkeep
```

## 部署 GitHub Pages
1. 在 GitHub 新建仓库，把此目录里的全部文件上传到仓库根目录。
2. 打开 Settings → Pages。
3. Build and deployment 选择 **Deploy from a branch**。
4. Branch 选择 `main`，目录选择 `/site`，保存。
5. 打开 Actions 标签，进入 **Update radar image** 工作流，点击 **Run workflow**。
6. 等待任务成功后，查看 `site/data/hko-radar.png` 是否被提交。
7. 打开 Pages 网站。首次运行前图像可能暂不可用；运行成功后网页从同源 `data/hko-radar.png` 读取已验证 PNG。
8. Actions 定时任务计划每 10 分钟执行一次；GitHub 的 schedule 不是精确实时调度，可能延迟。香港官方图像本身约每 6 分钟更新，因此实际新鲜度还受源站和调度延迟影响。

## 权限/限制
- 仓库 Actions 需要有写入仓库内容的权限。Settings → Actions → General → Workflow permissions 设为 **Read and write permissions**。
- 如果 GitHub Pages 发布源为 `/site`，只有 `site/` 内文件对外发布；脚本和工作流仍保存在仓库中。
- 本项目没有绕过登录、验证码或访问控制；仅读取公开雷达资源。
- GitHub Actions 抓取脚本不提供历史帧归档。每次成功运行会覆盖最新图像，提交历史可能保留部分更新记录，但不作为正式历史雷达服务。
- 澳门接口未接通，自定义双源动画/历史时次未实现。完成澳门原始图片地址验证后，才可补上第二个真实源。

## 官方入口
- 香港天文台雷达：https://www.hko.gov.hk/tc/wxinfo/radars/radar_range1.htm
- HKO 256 km KML 索引：https://www.hko.gov.hk/wxinfo/radars/R4_GIS_rad_256/R4_GIS_server_Radar_256.kml
- 澳门气象局雷达页面：https://www.dsmg.gov.mo/zh-hant/monitoring-images?slug=radarMap
