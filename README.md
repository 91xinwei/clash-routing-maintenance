# Clash 分流维护

面向 Clash Verge Rev / Mihomo，以及支持 rule-providers 的 Clash 内核。Flash 的具体产品和内核尚未确认，不承诺兼容。

## 推荐：保留现有订阅与策略组

安装 Python 依赖 `python3 -m pip install pyyaml`，然后运行：

```sh
python3 scripts/merge.py '/你的运行配置.yaml' merged.local.yaml
```

在客户端导入生成的本地文件并选择 Claude 策略组的固定节点。脚本优先复用现有 Claude 组，只将 Claude 核心规则置顶，保留其余配置。输出包含原有节点凭据，禁止上传。不要直接覆盖客户端自动生成文件；后续订阅刷新可能覆盖修改，建议将规则加入客户端覆写配置。

## 通用示例

`config.example.yaml` 提供国内直连、广告拦截、境外代理及 Claude 独立策略。必须自行加入节点并将 Proxy 组的 REJECT 替换为节点名称后才能使用。示例故意不包含订阅和节点，默认拒绝未配置的代理流量。

`rules/claude.yaml` 为核心及认证域名；`rules/claude-optional.yaml` 为共享遥测/客服域名，默认不启用，以免影响其他服务。优先使用固定、可用的 Claude 出口，规则本身不能保证账号风控结果或 DNS 隐私。

## 来源与取舍

- https://ip.net.coffee/claude/site.html ：参考核心、认证、CDN 和可选第三方域名。
- https://github.com/Loyalsoldier/clash-rules ：通用规则提供者，客户端每 24 小时更新缓存。
- https://github.com/MetaCubeX/meta-rules-dat ：调研了 Mihomo 专用格式；本示例采用 YAML 以扩大兼容范围。

未照搬网页的广泛 datadog/sift 关键词及 ASN 兜底。NTP 提供时间同步而非所在时区，未采用网页关于 NTP 返回时区的推断。未修改本机正在使用的配置。

## 验证

导入前运行 `mihomo -t -f merged.local.yaml`；导入后在连接面板检查 claude.ai、api.anthropic.com、anthropic.auth0.com 命中 Claude 组并使用预期出口。YAML 解析检查不等同于实际网络验证。

## 完整分类分流

现已提供 OpenAI、Gemini、Claude、GitHub、Telegram、YouTube、Netflix、Disney、Spotify、Discord、TikTok、Steam、Epic、Apple、Microsoft、Google、BiliBili 独立策略组。应用分类来自 blackmatrix7/ios_rule_script，国内/国外及广告兜底来自 Loyalsoldier。

Apple、Microsoft、Steam、Epic、BiliBili 默认直连，可在策略组中切换代理；其他海外服务默认代理。Gemini、YouTube 等细分类优先于 Google 总规则。各远程规则由客户端每 24 小时拉取更新。

合并脚本已扩展为完整分流：复用名称匹配的原有组，缺失组以 Routing 前缀创建；原有个人规则优先于新增通用规则，Claude 核心规则置顶。原有个人规则若包含宽泛的 Google/国外/国内规则，可能提前截获新分类，请在连接面板检查命中规则，必要时调整个人规则顺序。模板独立使用时分类优先级完整生效。

新增上游：https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash 。16 个远程分类地址已实际下载并验证 payload 非空。
