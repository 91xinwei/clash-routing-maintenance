# Clash 分流维护

一个「手动选择」组，所有代理服务跟随所选节点。无自动切换、无 DIRECT 备选；所选节点不可用时代理连接失败。国内与局域网按规则直连，广告拒绝，未知流量默认走代理。

## 融合来源

- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)：国内直连、境外代理、局域网、国内 IP、广告拦截基础集合。
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)：OpenAI、Gemini、GitHub、Telegram、YouTube、Netflix、Disney、Spotify、Discord、TikTok、Steam、Epic、Apple、Microsoft、Google、BiliBili 精细分类。海外分类统一指向手动选择，BiliBili 直连。
- [Net.Coffee](https://ip.net.coffee/claude/site.html)：Claude 核心及认证域名补充。
- [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)：已对比，其来源与上述集合有重叠，暂不叠加专用 MRS 数据，保持 YAML 规则兼容性。

融合采用远程 RULE-SET 引用，不复制整份第三方数据。客户端每24小时更新缓存。优先级：局域网 → Claude核心 → 精细服务 → 广告 → 国内域名 → 国外域名 → 国内IP → 默认代理。服务规则优先避免 AI/登录服务被泛化国内规则截走；可选共享遥测规则默认不开启。

## 使用现有节点

安装 PyYAML 后执行：

```sh
python3 scripts/merge.py '/你的完整运行配置.yaml' merged.local.yaml
```

脚本保留节点、订阅提供方及其他运行设置，替换旧策略组和路由为上述单组方案。输出包含私人节点信息，禁止上传。导入客户端后在「手动选择」中选节点。示例只有 REJECT 占位，独立使用前必须加入真实节点。

节点提供方应只包含真实代理节点；若订阅中包含 direct 类型节点，请先排除。自定义 DNS 若显式引用旧策略组，需要同步修改。规则仅处理客户端接管的流量，不能阻断其他应用绕过客户端的网络连接。

适配 Clash Verge Rev/Mihomo 及支持 YAML rule-providers 的 Clash 内核。Flash 产品及内核未确认。未修改本机在用配置。

## 验证

生成后运行 `mihomo -t -f merged.local.yaml`。在连接面板检查国内直连、海外命中手动选择；选择不可用节点后确认海外请求失败。仓库验证脚本检查远程规则可下载、payload非空及单组策略，不替代实际网络验证。
