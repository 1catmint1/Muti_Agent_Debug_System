# 🧾 Multi-Agent 详细修复报告

**生成时间**：2025-11-22 06:50:03.586298

---

## 🔍 扫描结果（详细）

### 🐛 内置规则缺陷（0 个）

### 🔧 外部工具执行情况

### ⚠️ 动态编译错误


## 📊 分析阶段

内容：
```json
{
  "summary": {
    "total_languages": 1,
    "total_issues": 85,
    "high_priority": 2,
    "medium_priority": 7,
    "low_priority": 76
  },
  "by_language": {
    "python": {
      "total": 85,
      "issues_by_file": {
        "arena.py": [
          {
            "file": "arena.py",
            "line": 12,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
            "snippet": "        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)",
            "count": 1,
            "examples": []
          },
          {
            "file": "arena.py",
            "line": 41,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY010",
            "message": "使用裸 except，建议捕获具体异常类型。",
            "snippet": "        except:",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 20,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\n\nimport define\nfrom dot import Dot\nfrom snake import Snake\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 8
                  },
                  "location": {
                    "column": 1,
                    "row": 1
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 1
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 1,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E501",
            "end_location": {
              "column": 93,
              "row": 13
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": null,
            "location": {
              "column": 89,
              "row": 13
            },
            "message": "Line too long (92 > 88)",
            "noqa_row": 13,
            "url": "https://docs.astral.sh/ruff/rules/line-too-long",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 22
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 22
                  },
                  "location": {
                    "column": 13,
                    "row": 22
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 22
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 22,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 27
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 27
                  },
                  "location": {
                    "column": 13,
                    "row": 27
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 27
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 27,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E722",
            "end_location": {
              "column": 15,
              "row": 41
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 41
            },
            "message": "Do not use bare `except`",
            "noqa_row": 41,
            "url": "https://docs.astral.sh/ruff/rules/bare-except",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.__init__",
            "line": 22,
            "column": 12,
            "endLine": 22,
            "endColumn": 13,
            "path": "arena.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'i'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.add_enemy",
            "line": 41,
            "column": 8,
            "endLine": 43,
            "endColumn": 16,
            "path": "arena.py",
            "symbol": "bare-except",
            "message": "No exception type(s) specified",
            "message-id": "W0702",
            "tool": "pylint"
          },
          {
            "type": "error",
            "module": "arena",
            "obj": "Arena.add_enemy",
            "line": 40,
            "column": 34,
            "endLine": 40,
            "endColumn": 61,
            "path": "arena.py",
            "symbol": "no-member",
            "message": "Instance of 'Snake' has no 'nonexistent_attribute' member",
            "message-id": "E1101",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.update",
            "line": 45,
            "column": 21,
            "endLine": 45,
            "endColumn": 23,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.on_key_press",
            "line": 49,
            "column": 32,
            "endLine": 49,
            "endColumn": 41,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.on_key_release",
            "line": 53,
            "column": 35,
            "endLine": 53,
            "endColumn": 44,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "code": "40             enemy.optional_attr = enemy.nonexistent_attribute\n41         except:\n42             # swallow everything deliberately\n43             pass\n44 \n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 41,
            "line_range": [
              41,
              42,
              43
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          }
        ],
        "dot.py": [
          {
            "file": "dot.py",
            "line": 13,
            "col": 24,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'Dot'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "        arena.batch.add(Dot())",
            "count": 2,
            "examples": [
              13,
              27
            ]
          },
          {
            "file": "dot.py",
            "line": 24,
            "col": 11,
            "severity": "MEDIUM",
            "rule_id": "AST002",
            "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。  （合并 2 条相似问题）",
            "snippet": "        if color is None:",
            "count": 2,
            "examples": [
              24,
              38
            ]
          },
          {
            "file": "dot.py",
            "line": 35,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "        except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 14,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import random\n\nfrom cocos.actions import CallFuncS, MoveTo\nfrom cocos.sprite import Sprite\n\nimport define\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 9
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.__init__",
            "line": 35,
            "column": 15,
            "endLine": 35,
            "endColumn": 24,
            "path": "dot.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.update",
            "line": 49,
            "column": 21,
            "endLine": 49,
            "endColumn": 23,
            "path": "dot.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.check_kill",
            "line": 61,
            "column": 12,
            "endLine": 61,
            "endColumn": 23,
            "path": "dot.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'killer' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "code": "24         if color is None:\n25             color = random.choice(define.ALL_COLOR)\n26 \n",
            "col_offset": 20,
            "end_col_offset": 51,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 25,
            "line_range": [
              25
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "34             # no f.close() here — deliberate\n35         except Exception:\n36             # ignore file errors intentionally\n37             pass\n38         if pos is None:\n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 35,
            "line_range": [
              35,
              36,
              37
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          },
          {
            "code": "38         if pos is None:\n39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n",
            "col_offset": 29,
            "end_col_offset": 66,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 39,
            "line_range": [
              39
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n41             self.is_big = False\n",
            "col_offset": 29,
            "end_col_offset": 67,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 40,
            "line_range": [
              40
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "43         else:\n44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n",
            "col_offset": 38,
            "end_col_offset": 53,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 44,
            "line_range": [
              44
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n46             self.is_big = True\n",
            "col_offset": 38,
            "end_col_offset": 53,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 45,
            "line_range": [
              45
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "46             self.is_big = True\n47         self.schedule_interval(self.update, random.random() * 0.2 + 0.1)\n48 \n",
            "col_offset": 44,
            "end_col_offset": 59,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 47,
            "line_range": [
              47
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          }
        ],
        "gameover.py": [
          {
            "file": "gameover.py",
            "line": 8,
            "col": 4,
            "severity": "HIGH",
            "rule_id": "AST001",
            "message": "函数 __init__ 的默认参数为可变对象，所有调用将共享同一对象。",
            "snippet": "    def __init__(self, banners=[]):",
            "count": 1,
            "examples": []
          },
          {
            "file": "gameover.py",
            "line": 11,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
            "snippet": "        super(Gameover, self).__init__(200, 235, 235, 200, 400, 300)",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 14,
              "row": 4
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\n\nimport define\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 6
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B006",
            "end_location": {
              "column": 34,
              "row": 8
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "None",
                  "end_location": {
                    "column": 34,
                    "row": 8
                  },
                  "location": {
                    "column": 32,
                    "row": 8
                  }
                },
                {
                  "content": "        if banners is None:\n            banners = []\n",
                  "end_location": {
                    "column": 1,
                    "row": 10
                  },
                  "location": {
                    "column": 1,
                    "row": 10
                  }
                }
              ],
              "message": "Replace with `None`; initialize within function"
            },
            "location": {
              "column": 32,
              "row": 8
            },
            "message": "Do not use mutable data structures for argument defaults",
            "noqa_row": 8,
            "url": "https://docs.astral.sh/ruff/rules/mutable-argument-default",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "gameover",
            "obj": "Gameover.__init__",
            "line": 8,
            "column": 4,
            "endLine": 8,
            "endColumn": 16,
            "path": "gameover.py",
            "symbol": "dangerous-default-value",
            "message": "Dangerous default value [] as argument",
            "message-id": "W0102",
            "tool": "pylint"
          }
        ],
        "gluttonous.py": [
          {
            "file": "gluttonous.py",
            "line": 3,
            "col": 0,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'cocos'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "cocos.audio.initialize = lambda *args, **kwargs: None  # 空函数",
            "count": 2,
            "examples": [
              3,
              27
            ]
          },
          {
            "file": "gluttonous.py",
            "line": 19,
            "col": 19,
            "severity": "HIGH",
            "rule_id": "PY001",
            "message": "使用 eval 可能导致代码执行漏洞。",
            "snippet": "            return eval(expr)",
            "count": 1,
            "examples": []
          },
          {
            "file": "gluttonous.py",
            "line": 20,
            "col": 4,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "    except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 19,
              "row": 2
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos.audio\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 3
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 13,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 6
            },
            "message": "Module level import not at top of file",
            "noqa_row": 6,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 30,
              "row": 12
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\nfrom cocos.scene import Scene\n\nimport define\nfrom arena import Arena\nfrom gameover import Gameover\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 14
                  },
                  "location": {
                    "column": 1,
                    "row": 6
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 6
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 6,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 36,
              "row": 7
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 7
            },
            "message": "Module level import not at top of file",
            "noqa_row": 7,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 30,
              "row": 8
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 8
            },
            "message": "Module level import not at top of file",
            "noqa_row": 8,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 14,
              "row": 10
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 10
            },
            "message": "Module level import not at top of file",
            "noqa_row": 10,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 24,
              "row": 11
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 11
            },
            "message": "Module level import not at top of file",
            "noqa_row": 11,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 30,
              "row": 12
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 12
            },
            "message": "Module level import not at top of file",
            "noqa_row": 12,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "W292",
            "end_location": {
              "column": 34,
              "row": 59
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "\n",
                  "end_location": {
                    "column": 34,
                    "row": 59
                  },
                  "location": {
                    "column": 34,
                    "row": 59
                  }
                }
              ],
              "message": "Add trailing newline"
            },
            "location": {
              "column": 34,
              "row": 59
            },
            "message": "No newline at end of file",
            "noqa_row": 59,
            "url": "https://docs.astral.sh/ruff/rules/missing-newline-at-end-of-file",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "unsafe_eval",
            "line": 20,
            "column": 11,
            "endLine": 20,
            "endColumn": 20,
            "path": "gluttonous.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "unsafe_eval",
            "line": 19,
            "column": 19,
            "endLine": 19,
            "endColumn": 29,
            "path": "gluttonous.py",
            "symbol": "eval-used",
            "message": "Use of eval",
            "message-id": "W0123",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 29,
            "endLine": 48,
            "endColumn": 30,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'x'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 32,
            "endLine": 48,
            "endColumn": 33,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'y'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 35,
            "endLine": 48,
            "endColumn": 42,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'buttons'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 44,
            "endLine": 48,
            "endColumn": 53,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "code": "18         if isinstance(expr, str) and len(expr) < 50:\n19             return eval(expr)\n20     except Exception:\n",
            "col_offset": 19,
            "end_col_offset": 29,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 78,
              "link": "https://cwe.mitre.org/data/definitions/78.html"
            },
            "issue_severity": "MEDIUM",
            "issue_text": "Use of possibly insecure function - consider using safer ast.literal_eval.",
            "line_number": 19,
            "line_range": [
              19
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b307-eval",
            "test_id": "B307",
            "test_name": "blacklist",
            "tool": "bandit"
          }
        ],
        "snake.py": [
          {
            "file": "snake.py",
            "line": 16,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "        super(Snake, self).__init__()",
            "count": 2,
            "examples": [
              16,
              113
            ]
          },
          {
            "file": "snake.py",
            "line": 65,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "        except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "file": "snake.py",
            "line": 77,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY010",
            "message": "使用裸 except，建议捕获具体异常类型。",
            "snippet": "        except:",
            "count": 1,
            "examples": []
          },
          {
            "file": "snake.py",
            "line": 135,
            "col": 11,
            "severity": "MEDIUM",
            "rule_id": "AST002",
            "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。",
            "snippet": "        if direct is None:",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 20,
              "row": 9
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import math\nimport os  # Intentional: unused import to be flagged by linters\nimport random\n\nimport cocos\nfrom cocos.sprite import Sprite\n\nimport define\nfrom dot import Dot\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 12
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "F401",
            "end_location": {
              "column": 10,
              "row": 3
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 4
                  },
                  "location": {
                    "column": 1,
                    "row": 3
                  }
                }
              ],
              "message": "Remove unused import: `os`"
            },
            "location": {
              "column": 8,
              "row": 3
            },
            "message": "`os` imported but unused",
            "noqa_row": 3,
            "url": "https://docs.astral.sh/ruff/rules/unused-import",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "F841",
            "end_location": {
              "column": 13,
              "row": 68
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 69
                  },
                  "location": {
                    "column": 1,
                    "row": 68
                  }
                }
              ],
              "message": "Remove assignment to unused variable `list`"
            },
            "location": {
              "column": 9,
              "row": 68
            },
            "message": "Local variable `list` is assigned to but never used",
            "noqa_row": 68,
            "url": "https://docs.astral.sh/ruff/rules/unused-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E722",
            "end_location": {
              "column": 15,
              "row": 77
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 77
            },
            "message": "Do not use bare `except`",
            "noqa_row": 77,
            "url": "https://docs.astral.sh/ruff/rules/bare-except",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 84
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 84
                  },
                  "location": {
                    "column": 13,
                    "row": 84
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 84
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 84,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E741",
            "end_location": {
              "column": 10,
              "row": 144
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 144
            },
            "message": "Ambiguous variable name: `l`",
            "noqa_row": 144,
            "url": "https://docs.astral.sh/ruff/rules/ambiguous-variable-name",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 68,
            "column": 8,
            "endLine": 68,
            "endColumn": 12,
            "path": "snake.py",
            "symbol": "redefined-builtin",
            "message": "Redefining built-in 'list'",
            "message-id": "W0622",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 65,
            "column": 15,
            "endLine": 65,
            "endColumn": 24,
            "path": "snake.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 77,
            "column": 8,
            "endLine": 78,
            "endColumn": 53,
            "path": "snake.py",
            "symbol": "bare-except",
            "message": "No exception type(s) specified",
            "message-id": "W0702",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 68,
            "column": 8,
            "endLine": 68,
            "endColumn": 12,
            "path": "snake.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'list'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 84,
            "column": 12,
            "endLine": 84,
            "endColumn": 13,
            "path": "snake.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'i'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.ai",
            "line": 149,
            "column": 17,
            "endLine": 149,
            "endColumn": 19,
            "path": "snake.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 63,
            "column": 16,
            "endLine": 63,
            "endColumn": 31,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute '_tmp_store' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 81,
            "column": 8,
            "endLine": 81,
            "endColumn": 18,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'score' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 82,
            "column": 8,
            "endLine": 82,
            "endColumn": 19,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'length' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_score",
            "line": 146,
            "column": 12,
            "endLine": 146,
            "endColumn": 23,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'length' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 83,
            "column": 8,
            "endLine": 83,
            "endColumn": 17,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'body' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "",
            "line": 3,
            "column": 0,
            "endLine": 3,
            "endColumn": 9,
            "path": "snake.py",
            "symbol": "unused-import",
            "message": "Unused import os",
            "message-id": "W0611",
            "tool": "pylint"
          },
          {
            "code": "17         self.is_dead = False\n18         self.angle = random.randrange(360)  # 目前角度\n19         self.angle_dest = self.angle  # 目标角度\n",
            "col_offset": 21,
            "end_col_offset": 42,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 18,
            "line_range": [
              18
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "19         self.angle_dest = self.angle  # 目标角度\n20         self.color = random.choice(define.ALL_COLOR)\n21         self.no = Snake.no\n",
            "col_offset": 21,
            "end_col_offset": 52,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 20,
            "line_range": [
              20
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
            "col_offset": 28,
            "end_col_offset": 55,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 24,
            "line_range": [
              24
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
            "col_offset": 57,
            "end_col_offset": 83,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 24,
            "line_range": [
              24
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
            "col_offset": 28,
            "end_col_offset": 54,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 28,
            "line_range": [
              28
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
            "col_offset": 56,
            "end_col_offset": 82,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 28,
            "line_range": [
              28
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "55         if self.is_enemy:\n56             self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)\n57 \n",
            "col_offset": 44,
            "end_col_offset": 59,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 56,
            "line_range": [
              56
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "64             self._tmp_store.append(self.color)\n65         except Exception:\n66             pass\n67         # Intentional: shadow built-in name to create a detectable smell\n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 65,
            "line_range": [
              65,
              66
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          },
          {
            "code": "185             if abs(angle - self.angle_dest) < 5:\n186                 self.angle_dest += random.randrange(90, 270)\n187 \n",
            "col_offset": 35,
            "end_col_offset": 60,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 186,
            "line_range": [
              186
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          }
        ],
        "define.py": [
          {
            "cell": null,
            "code": "F401",
            "end_location": {
              "column": 14,
              "row": 2
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\define.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 3
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Remove unused import: `random`"
            },
            "location": {
              "column": 8,
              "row": 2
            },
            "message": "`random` imported but unused",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unused-import",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "define",
            "obj": "",
            "line": 2,
            "column": 0,
            "endLine": 2,
            "endColumn": 13,
            "path": "define.py",
            "symbol": "unused-import",
            "message": "Unused import random",
            "message-id": "W0611",
            "tool": "pylint"
          }
        ]
      },
      "issues_by_severity": {
        "HIGH": [
          {
            "file": "gameover.py",
            "line": 8,
            "col": 4,
            "severity": "HIGH",
            "rule_id": "AST001",
            "message": "函数 __init__ 的默认参数为可变对象，所有调用将共享同一对象。",
            "snippet": "    def __init__(self, banners=[]):",
            "count": 1,
            "examples": []
          },
          {
            "file": "gluttonous.py",
            "line": 19,
            "col": 19,
            "severity": "HIGH",
            "rule_id": "PY001",
            "message": "使用 eval 可能导致代码执行漏洞。",
            "snippet": "            return eval(expr)",
            "count": 1,
            "examples": []
          }
        ],
        "MEDIUM": [
          {
            "file": "arena.py",
            "line": 12,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
            "snippet": "        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)",
            "count": 1,
            "examples": []
          },
          {
            "file": "dot.py",
            "line": 13,
            "col": 24,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'Dot'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "        arena.batch.add(Dot())",
            "count": 2,
            "examples": [
              13,
              27
            ]
          },
          {
            "file": "dot.py",
            "line": 24,
            "col": 11,
            "severity": "MEDIUM",
            "rule_id": "AST002",
            "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。  （合并 2 条相似问题）",
            "snippet": "        if color is None:",
            "count": 2,
            "examples": [
              24,
              38
            ]
          },
          {
            "file": "gameover.py",
            "line": 11,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
            "snippet": "        super(Gameover, self).__init__(200, 235, 235, 200, 400, 300)",
            "count": 1,
            "examples": []
          },
          {
            "file": "gluttonous.py",
            "line": 3,
            "col": 0,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'cocos'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "cocos.audio.initialize = lambda *args, **kwargs: None  # 空函数",
            "count": 2,
            "examples": [
              3,
              27
            ]
          },
          {
            "file": "snake.py",
            "line": 16,
            "col": 8,
            "severity": "MEDIUM",
            "rule_id": "PY100",
            "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
            "snippet": "        super(Snake, self).__init__()",
            "count": 2,
            "examples": [
              16,
              113
            ]
          },
          {
            "file": "snake.py",
            "line": 135,
            "col": 11,
            "severity": "MEDIUM",
            "rule_id": "AST002",
            "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。",
            "snippet": "        if direct is None:",
            "count": 1,
            "examples": []
          }
        ],
        "LOW": [
          {
            "file": "arena.py",
            "line": 41,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY010",
            "message": "使用裸 except，建议捕获具体异常类型。",
            "snippet": "        except:",
            "count": 1,
            "examples": []
          },
          {
            "file": "dot.py",
            "line": 35,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "        except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "file": "gluttonous.py",
            "line": 20,
            "col": 4,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "    except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "file": "snake.py",
            "line": 65,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY011",
            "message": "过于宽泛的异常捕获：Exception。",
            "snippet": "        except Exception:",
            "count": 1,
            "examples": []
          },
          {
            "file": "snake.py",
            "line": 77,
            "col": 8,
            "severity": "LOW",
            "rule_id": "PY010",
            "message": "使用裸 except，建议捕获具体异常类型。",
            "snippet": "        except:",
            "count": 1,
            "examples": []
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 20,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\n\nimport define\nfrom dot import Dot\nfrom snake import Snake\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 8
                  },
                  "location": {
                    "column": 1,
                    "row": 1
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 1
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 1,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E501",
            "end_location": {
              "column": 93,
              "row": 13
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": null,
            "location": {
              "column": 89,
              "row": 13
            },
            "message": "Line too long (92 > 88)",
            "noqa_row": 13,
            "url": "https://docs.astral.sh/ruff/rules/line-too-long",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 22
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 22
                  },
                  "location": {
                    "column": 13,
                    "row": 22
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 22
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 22,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 27
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 27
                  },
                  "location": {
                    "column": 13,
                    "row": 27
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 27
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 27,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E722",
            "end_location": {
              "column": 15,
              "row": 41
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 41
            },
            "message": "Do not use bare `except`",
            "noqa_row": 41,
            "url": "https://docs.astral.sh/ruff/rules/bare-except",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "F401",
            "end_location": {
              "column": 14,
              "row": 2
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\define.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 3
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Remove unused import: `random`"
            },
            "location": {
              "column": 8,
              "row": 2
            },
            "message": "`random` imported but unused",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unused-import",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 14,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import random\n\nfrom cocos.actions import CallFuncS, MoveTo\nfrom cocos.sprite import Sprite\n\nimport define\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 9
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 14,
              "row": 4
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\n\nimport define\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 6
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B006",
            "end_location": {
              "column": 34,
              "row": 8
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "None",
                  "end_location": {
                    "column": 34,
                    "row": 8
                  },
                  "location": {
                    "column": 32,
                    "row": 8
                  }
                },
                {
                  "content": "        if banners is None:\n            banners = []\n",
                  "end_location": {
                    "column": 1,
                    "row": 10
                  },
                  "location": {
                    "column": 1,
                    "row": 10
                  }
                }
              ],
              "message": "Replace with `None`; initialize within function"
            },
            "location": {
              "column": 32,
              "row": 8
            },
            "message": "Do not use mutable data structures for argument defaults",
            "noqa_row": 8,
            "url": "https://docs.astral.sh/ruff/rules/mutable-argument-default",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 19,
              "row": 2
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos.audio\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 3
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 13,
              "row": 6
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 6
            },
            "message": "Module level import not at top of file",
            "noqa_row": 6,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 30,
              "row": 12
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import cocos\nfrom cocos.director import director\nfrom cocos.scene import Scene\n\nimport define\nfrom arena import Arena\nfrom gameover import Gameover\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 14
                  },
                  "location": {
                    "column": 1,
                    "row": 6
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 6
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 6,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 36,
              "row": 7
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 7
            },
            "message": "Module level import not at top of file",
            "noqa_row": 7,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 30,
              "row": 8
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 8
            },
            "message": "Module level import not at top of file",
            "noqa_row": 8,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 14,
              "row": 10
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 10
            },
            "message": "Module level import not at top of file",
            "noqa_row": 10,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 24,
              "row": 11
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 11
            },
            "message": "Module level import not at top of file",
            "noqa_row": 11,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E402",
            "end_location": {
              "column": 30,
              "row": 12
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": null,
            "location": {
              "column": 1,
              "row": 12
            },
            "message": "Module level import not at top of file",
            "noqa_row": 12,
            "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "W292",
            "end_location": {
              "column": 34,
              "row": 59
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "\n",
                  "end_location": {
                    "column": 34,
                    "row": 59
                  },
                  "location": {
                    "column": 34,
                    "row": 59
                  }
                }
              ],
              "message": "Add trailing newline"
            },
            "location": {
              "column": 34,
              "row": 59
            },
            "message": "No newline at end of file",
            "noqa_row": 59,
            "url": "https://docs.astral.sh/ruff/rules/missing-newline-at-end-of-file",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "I001",
            "end_location": {
              "column": 20,
              "row": 9
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "import math\nimport os  # Intentional: unused import to be flagged by linters\nimport random\n\nimport cocos\nfrom cocos.sprite import Sprite\n\nimport define\nfrom dot import Dot\n\n\n",
                  "end_location": {
                    "column": 1,
                    "row": 12
                  },
                  "location": {
                    "column": 1,
                    "row": 2
                  }
                }
              ],
              "message": "Organize imports"
            },
            "location": {
              "column": 1,
              "row": 2
            },
            "message": "Import block is un-sorted or un-formatted",
            "noqa_row": 2,
            "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "F401",
            "end_location": {
              "column": 10,
              "row": 3
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "safe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 4
                  },
                  "location": {
                    "column": 1,
                    "row": 3
                  }
                }
              ],
              "message": "Remove unused import: `os`"
            },
            "location": {
              "column": 8,
              "row": 3
            },
            "message": "`os` imported but unused",
            "noqa_row": 3,
            "url": "https://docs.astral.sh/ruff/rules/unused-import",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "F841",
            "end_location": {
              "column": 13,
              "row": 68
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "",
                  "end_location": {
                    "column": 1,
                    "row": 69
                  },
                  "location": {
                    "column": 1,
                    "row": 68
                  }
                }
              ],
              "message": "Remove assignment to unused variable `list`"
            },
            "location": {
              "column": 9,
              "row": 68
            },
            "message": "Local variable `list` is assigned to but never used",
            "noqa_row": 68,
            "url": "https://docs.astral.sh/ruff/rules/unused-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E722",
            "end_location": {
              "column": 15,
              "row": 77
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 77
            },
            "message": "Do not use bare `except`",
            "noqa_row": 77,
            "url": "https://docs.astral.sh/ruff/rules/bare-except",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "B007",
            "end_location": {
              "column": 14,
              "row": 84
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": {
              "applicability": "unsafe",
              "edits": [
                {
                  "content": "_i",
                  "end_location": {
                    "column": 14,
                    "row": 84
                  },
                  "location": {
                    "column": 13,
                    "row": 84
                  }
                }
              ],
              "message": "Rename unused `i` to `_i`"
            },
            "location": {
              "column": 13,
              "row": 84
            },
            "message": "Loop control variable `i` not used within loop body",
            "noqa_row": 84,
            "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
            "tool": "ruff"
          },
          {
            "cell": null,
            "code": "E741",
            "end_location": {
              "column": 10,
              "row": 144
            },
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "fix": null,
            "location": {
              "column": 9,
              "row": 144
            },
            "message": "Ambiguous variable name: `l`",
            "noqa_row": 144,
            "url": "https://docs.astral.sh/ruff/rules/ambiguous-variable-name",
            "tool": "ruff"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.__init__",
            "line": 22,
            "column": 12,
            "endLine": 22,
            "endColumn": 13,
            "path": "arena.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'i'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.add_enemy",
            "line": 41,
            "column": 8,
            "endLine": 43,
            "endColumn": 16,
            "path": "arena.py",
            "symbol": "bare-except",
            "message": "No exception type(s) specified",
            "message-id": "W0702",
            "tool": "pylint"
          },
          {
            "type": "error",
            "module": "arena",
            "obj": "Arena.add_enemy",
            "line": 40,
            "column": 34,
            "endLine": 40,
            "endColumn": 61,
            "path": "arena.py",
            "symbol": "no-member",
            "message": "Instance of 'Snake' has no 'nonexistent_attribute' member",
            "message-id": "E1101",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.update",
            "line": 45,
            "column": 21,
            "endLine": 45,
            "endColumn": 23,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.on_key_press",
            "line": 49,
            "column": 32,
            "endLine": 49,
            "endColumn": 41,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "arena",
            "obj": "Arena.on_key_release",
            "line": 53,
            "column": 35,
            "endLine": 53,
            "endColumn": 44,
            "path": "arena.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "define",
            "obj": "",
            "line": 2,
            "column": 0,
            "endLine": 2,
            "endColumn": 13,
            "path": "define.py",
            "symbol": "unused-import",
            "message": "Unused import random",
            "message-id": "W0611",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.__init__",
            "line": 35,
            "column": 15,
            "endLine": 35,
            "endColumn": 24,
            "path": "dot.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.update",
            "line": 49,
            "column": 21,
            "endLine": 49,
            "endColumn": 23,
            "path": "dot.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "dot",
            "obj": "Dot.check_kill",
            "line": 61,
            "column": 12,
            "endLine": 61,
            "endColumn": 23,
            "path": "dot.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'killer' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gameover",
            "obj": "Gameover.__init__",
            "line": 8,
            "column": 4,
            "endLine": 8,
            "endColumn": 16,
            "path": "gameover.py",
            "symbol": "dangerous-default-value",
            "message": "Dangerous default value [] as argument",
            "message-id": "W0102",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "unsafe_eval",
            "line": 20,
            "column": 11,
            "endLine": 20,
            "endColumn": 20,
            "path": "gluttonous.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "unsafe_eval",
            "line": 19,
            "column": 19,
            "endLine": 19,
            "endColumn": 29,
            "path": "gluttonous.py",
            "symbol": "eval-used",
            "message": "Use of eval",
            "message-id": "W0123",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 29,
            "endLine": 48,
            "endColumn": 30,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'x'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 32,
            "endLine": 48,
            "endColumn": 33,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'y'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 35,
            "endLine": 48,
            "endColumn": 42,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'buttons'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "gluttonous",
            "obj": "HelloWorld.on_mouse_press",
            "line": 48,
            "column": 44,
            "endLine": 48,
            "endColumn": 53,
            "path": "gluttonous.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'modifiers'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 68,
            "column": 8,
            "endLine": 68,
            "endColumn": 12,
            "path": "snake.py",
            "symbol": "redefined-builtin",
            "message": "Redefining built-in 'list'",
            "message-id": "W0622",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 65,
            "column": 15,
            "endLine": 65,
            "endColumn": 24,
            "path": "snake.py",
            "symbol": "broad-exception-caught",
            "message": "Catching too general exception Exception",
            "message-id": "W0718",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 77,
            "column": 8,
            "endLine": 78,
            "endColumn": 53,
            "path": "snake.py",
            "symbol": "bare-except",
            "message": "No exception type(s) specified",
            "message-id": "W0702",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 68,
            "column": 8,
            "endLine": 68,
            "endColumn": 12,
            "path": "snake.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'list'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 84,
            "column": 12,
            "endLine": 84,
            "endColumn": 13,
            "path": "snake.py",
            "symbol": "unused-variable",
            "message": "Unused variable 'i'",
            "message-id": "W0612",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.ai",
            "line": 149,
            "column": 17,
            "endLine": 149,
            "endColumn": 19,
            "path": "snake.py",
            "symbol": "unused-argument",
            "message": "Unused argument 'dt'",
            "message-id": "W0613",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_body",
            "line": 63,
            "column": 16,
            "endLine": 63,
            "endColumn": 31,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute '_tmp_store' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 81,
            "column": 8,
            "endLine": 81,
            "endColumn": 18,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'score' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 82,
            "column": 8,
            "endLine": 82,
            "endColumn": 19,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'length' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.add_score",
            "line": 146,
            "column": 12,
            "endLine": 146,
            "endColumn": 23,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'length' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "Snake.init_body",
            "line": 83,
            "column": 8,
            "endLine": 83,
            "endColumn": 17,
            "path": "snake.py",
            "symbol": "attribute-defined-outside-init",
            "message": "Attribute 'body' defined outside __init__",
            "message-id": "W0201",
            "tool": "pylint"
          },
          {
            "type": "warning",
            "module": "snake",
            "obj": "",
            "line": 3,
            "column": 0,
            "endLine": 3,
            "endColumn": 9,
            "path": "snake.py",
            "symbol": "unused-import",
            "message": "Unused import os",
            "message-id": "W0611",
            "tool": "pylint"
          },
          {
            "code": "40             enemy.optional_attr = enemy.nonexistent_attribute\n41         except:\n42             # swallow everything deliberately\n43             pass\n44 \n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 41,
            "line_range": [
              41,
              42,
              43
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          },
          {
            "code": "24         if color is None:\n25             color = random.choice(define.ALL_COLOR)\n26 \n",
            "col_offset": 20,
            "end_col_offset": 51,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 25,
            "line_range": [
              25
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "34             # no f.close() here — deliberate\n35         except Exception:\n36             # ignore file errors intentionally\n37             pass\n38         if pos is None:\n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 35,
            "line_range": [
              35,
              36,
              37
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          },
          {
            "code": "38         if pos is None:\n39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n",
            "col_offset": 29,
            "end_col_offset": 66,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 39,
            "line_range": [
              39
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n41             self.is_big = False\n",
            "col_offset": 29,
            "end_col_offset": 67,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 40,
            "line_range": [
              40
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "43         else:\n44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n",
            "col_offset": 38,
            "end_col_offset": 53,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 44,
            "line_range": [
              44
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n46             self.is_big = True\n",
            "col_offset": 38,
            "end_col_offset": 53,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 45,
            "line_range": [
              45
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "46             self.is_big = True\n47         self.schedule_interval(self.update, random.random() * 0.2 + 0.1)\n48 \n",
            "col_offset": 44,
            "end_col_offset": 59,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 47,
            "line_range": [
              47
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "18         if isinstance(expr, str) and len(expr) < 50:\n19             return eval(expr)\n20     except Exception:\n",
            "col_offset": 19,
            "end_col_offset": 29,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 78,
              "link": "https://cwe.mitre.org/data/definitions/78.html"
            },
            "issue_severity": "MEDIUM",
            "issue_text": "Use of possibly insecure function - consider using safer ast.literal_eval.",
            "line_number": 19,
            "line_range": [
              19
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b307-eval",
            "test_id": "B307",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "17         self.is_dead = False\n18         self.angle = random.randrange(360)  # 目前角度\n19         self.angle_dest = self.angle  # 目标角度\n",
            "col_offset": 21,
            "end_col_offset": 42,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 18,
            "line_range": [
              18
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "19         self.angle_dest = self.angle  # 目标角度\n20         self.color = random.choice(define.ALL_COLOR)\n21         self.no = Snake.no\n",
            "col_offset": 21,
            "end_col_offset": 52,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 20,
            "line_range": [
              20
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
            "col_offset": 28,
            "end_col_offset": 55,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 24,
            "line_range": [
              24
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
            "col_offset": 57,
            "end_col_offset": 83,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 24,
            "line_range": [
              24
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
            "col_offset": 28,
            "end_col_offset": 54,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 28,
            "line_range": [
              28
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
            "col_offset": 56,
            "end_col_offset": 82,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 28,
            "line_range": [
              28
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "55         if self.is_enemy:\n56             self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)\n57 \n",
            "col_offset": 44,
            "end_col_offset": 59,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 56,
            "line_range": [
              56
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          },
          {
            "code": "64             self._tmp_store.append(self.color)\n65         except Exception:\n66             pass\n67         # Intentional: shadow built-in name to create a detectable smell\n",
            "col_offset": 8,
            "end_col_offset": 16,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 703,
              "link": "https://cwe.mitre.org/data/definitions/703.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Try, Except, Pass detected.",
            "line_number": 65,
            "line_range": [
              65,
              66
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
            "test_id": "B110",
            "test_name": "try_except_pass",
            "tool": "bandit"
          },
          {
            "code": "185             if abs(angle - self.angle_dest) < 5:\n186                 self.angle_dest += random.randrange(90, 270)\n187 \n",
            "col_offset": 35,
            "end_col_offset": 60,
            "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {
              "id": 330,
              "link": "https://cwe.mitre.org/data/definitions/330.html"
            },
            "issue_severity": "LOW",
            "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
            "line_number": 186,
            "line_range": [
              186
            ],
            "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
            "test_id": "B311",
            "test_name": "blacklist",
            "tool": "bandit"
          }
        ]
      },
      "dynamic_check": {
        "py_compile": [],
        "pytest": {
          "skipped": true,
          "reason": "未配置测试"
        },
        "dynamic_detection": {
          "enabled": true,
          "categories": {
            "user_input": [],
            "resource_management": [
              {
                "file": "dot.py",
                "line": 32,
                "col": 16,
                "category": "resource_management",
                "severity": "HIGH",
                "rule_id": "DYN-RES-001",
                "message": "文件打开未使用 with 语句，可能导致资源泄漏",
                "snippet": "            f = open('getqrcode.jpeg', 'rb')",
                "suggestion": "使用 with open(...) as f: 确保文件自动关闭"
              }
            ],
            "concurrency": [],
            "boundary_conditions": [
              {
                "file": "arena.py",
                "line": 13,
                "col": 23,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "arena.py",
                "line": 13,
                "col": 58,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "gameover.py",
                "line": 12,
                "col": 25,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.position = (director.get_window_size()[0] / 2 - 200,",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "gameover.py",
                "line": 13,
                "col": 25,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                         director.get_window_size()[1] / 2 - 150)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 109,
                "col": 27,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 110,
                "col": 27,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 113,
                "col": 24,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        lag = int(round(1100.0 / self.speed))",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 114,
                "col": 8,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-001",
                "message": "循环中的数组访问可能越界",
                "snippet": "        for i in range(len(self.body)):",
                "suggestion": "确保索引在有效范围内，考虑使用 enumerate()"
              },
              {
                "file": "snake.py",
                "line": 144,
                "col": 12,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        l = (self.score - 6) / 6",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 181,
                "col": 24,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                angle = math.atan(d_y / d_x) * 180 / math.pi",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 181,
                "col": 34,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                angle = math.atan(d_y / d_x) * 180 / math.pi",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 197,
                "col": 28,
                "category": "boundary_conditions",
                "severity": "LOW",
                "rule_id": "DYN-BOUND-003",
                "message": "幂运算可能导致溢出",
                "snippet": "            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)",
                "suggestion": "检查输入范围，防止数值溢出"
              },
              {
                "file": "snake.py",
                "line": 197,
                "col": 50,
                "category": "boundary_conditions",
                "severity": "LOW",
                "rule_id": "DYN-BOUND-003",
                "message": "幂运算可能导致溢出",
                "snippet": "            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)",
                "suggestion": "检查输入范围，防止数值溢出"
              }
            ],
            "environment_config": [],
            "dynamic_execution": [
              {
                "file": "gluttonous.py",
                "line": 19,
                "col": 19,
                "category": "dynamic_execution",
                "severity": "HIGH",
                "rule_id": "DYN-EXEC-001",
                "message": "使用 eval() 存在代码注入风险",
                "snippet": "            return eval(expr)",
                "suggestion": "避免使用 eval/exec，或严格验证输入"
              }
            ]
          },
          "summary": {
            "total": 15,
            "by_category": {
              "resource_management": 1,
              "boundary_conditions": 13,
              "dynamic_execution": 1
            },
            "by_severity": {
              "HIGH": 2,
              "MEDIUM": 11,
              "LOW": 2
            }
          }
        }
      }
    }
  },
  "recommendations": [
    "⚠️ PYTHON: 发现 2 个高危问题，建议优先修复"
  ],
  "fix_plans": [
    {
      "language": "python",
      "total_issues": 85,
      "high": 2,
      "medium": 7,
      "low": 76,
      "priority_score": 131,
      "builtin_issues": [
        {
          "file": "arena.py",
          "line": 12,
          "col": 8,
          "severity": "MEDIUM",
          "rule_id": "PY100",
          "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
          "snippet": "        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)",
          "count": 1,
          "examples": []
        },
        {
          "file": "arena.py",
          "line": 41,
          "col": 8,
          "severity": "LOW",
          "rule_id": "PY010",
          "message": "使用裸 except，建议捕获具体异常类型。",
          "snippet": "        except:",
          "count": 1,
          "examples": []
        },
        {
          "file": "dot.py",
          "line": 13,
          "col": 24,
          "severity": "MEDIUM",
          "rule_id": "PY100",
          "message": "疑似使用了未定义的名称 'Dot'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
          "snippet": "        arena.batch.add(Dot())",
          "count": 2,
          "examples": [
            13,
            27
          ]
        },
        {
          "file": "dot.py",
          "line": 24,
          "col": 11,
          "severity": "MEDIUM",
          "rule_id": "AST002",
          "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。  （合并 2 条相似问题）",
          "snippet": "        if color is None:",
          "count": 2,
          "examples": [
            24,
            38
          ]
        },
        {
          "file": "dot.py",
          "line": 35,
          "col": 8,
          "severity": "LOW",
          "rule_id": "PY011",
          "message": "过于宽泛的异常捕获：Exception。",
          "snippet": "        except Exception:",
          "count": 1,
          "examples": []
        },
        {
          "file": "gameover.py",
          "line": 8,
          "col": 4,
          "severity": "HIGH",
          "rule_id": "AST001",
          "message": "函数 __init__ 的默认参数为可变对象，所有调用将共享同一对象。",
          "snippet": "    def __init__(self, banners=[]):",
          "count": 1,
          "examples": []
        },
        {
          "file": "gameover.py",
          "line": 11,
          "col": 8,
          "severity": "MEDIUM",
          "rule_id": "PY100",
          "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。",
          "snippet": "        super(Gameover, self).__init__(200, 235, 235, 200, 400, 300)",
          "count": 1,
          "examples": []
        },
        {
          "file": "gluttonous.py",
          "line": 3,
          "col": 0,
          "severity": "MEDIUM",
          "rule_id": "PY100",
          "message": "疑似使用了未定义的名称 'cocos'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
          "snippet": "cocos.audio.initialize = lambda *args, **kwargs: None  # 空函数",
          "count": 2,
          "examples": [
            3,
            27
          ]
        },
        {
          "file": "gluttonous.py",
          "line": 19,
          "col": 19,
          "severity": "HIGH",
          "rule_id": "PY001",
          "message": "使用 eval 可能导致代码执行漏洞。",
          "snippet": "            return eval(expr)",
          "count": 1,
          "examples": []
        },
        {
          "file": "gluttonous.py",
          "line": 20,
          "col": 4,
          "severity": "LOW",
          "rule_id": "PY011",
          "message": "过于宽泛的异常捕获：Exception。",
          "snippet": "    except Exception:",
          "count": 1,
          "examples": []
        },
        {
          "file": "snake.py",
          "line": 16,
          "col": 8,
          "severity": "MEDIUM",
          "rule_id": "PY100",
          "message": "疑似使用了未定义的名称 'super'（可能为动态导入或第三方库）。  （合并 2 条相似问题）",
          "snippet": "        super(Snake, self).__init__()",
          "count": 2,
          "examples": [
            16,
            113
          ]
        },
        {
          "file": "snake.py",
          "line": 65,
          "col": 8,
          "severity": "LOW",
          "rule_id": "PY011",
          "message": "过于宽泛的异常捕获：Exception。",
          "snippet": "        except Exception:",
          "count": 1,
          "examples": []
        },
        {
          "file": "snake.py",
          "line": 77,
          "col": 8,
          "severity": "LOW",
          "rule_id": "PY010",
          "message": "使用裸 except，建议捕获具体异常类型。",
          "snippet": "        except:",
          "count": 1,
          "examples": []
        },
        {
          "file": "snake.py",
          "line": 135,
          "col": 11,
          "severity": "MEDIUM",
          "rule_id": "AST002",
          "message": "疑似使用 'is' 进行值比较，建议使用 '==' （is 仅用于 None/True/False）。",
          "snippet": "        if direct is None:",
          "count": 1,
          "examples": []
        }
      ],
      "external_issues": [
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 20,
            "row": 6
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import cocos\nfrom cocos.director import director\n\nimport define\nfrom dot import Dot\nfrom snake import Snake\n\n\n",
                "end_location": {
                  "column": 1,
                  "row": 8
                },
                "location": {
                  "column": 1,
                  "row": 1
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 1
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 1,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E501",
          "end_location": {
            "column": 93,
            "row": 13
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "fix": null,
          "location": {
            "column": 89,
            "row": 13
          },
          "message": "Line too long (92 > 88)",
          "noqa_row": 13,
          "url": "https://docs.astral.sh/ruff/rules/line-too-long",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "B007",
          "end_location": {
            "column": 14,
            "row": 22
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "fix": {
            "applicability": "unsafe",
            "edits": [
              {
                "content": "_i",
                "end_location": {
                  "column": 14,
                  "row": 22
                },
                "location": {
                  "column": 13,
                  "row": 22
                }
              }
            ],
            "message": "Rename unused `i` to `_i`"
          },
          "location": {
            "column": 13,
            "row": 22
          },
          "message": "Loop control variable `i` not used within loop body",
          "noqa_row": 22,
          "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "B007",
          "end_location": {
            "column": 14,
            "row": 27
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "fix": {
            "applicability": "unsafe",
            "edits": [
              {
                "content": "_i",
                "end_location": {
                  "column": 14,
                  "row": 27
                },
                "location": {
                  "column": 13,
                  "row": 27
                }
              }
            ],
            "message": "Rename unused `i` to `_i`"
          },
          "location": {
            "column": 13,
            "row": 27
          },
          "message": "Loop control variable `i` not used within loop body",
          "noqa_row": 27,
          "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E722",
          "end_location": {
            "column": 15,
            "row": 41
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "fix": null,
          "location": {
            "column": 9,
            "row": 41
          },
          "message": "Do not use bare `except`",
          "noqa_row": 41,
          "url": "https://docs.astral.sh/ruff/rules/bare-except",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "F401",
          "end_location": {
            "column": 14,
            "row": 2
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\define.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "",
                "end_location": {
                  "column": 1,
                  "row": 3
                },
                "location": {
                  "column": 1,
                  "row": 2
                }
              }
            ],
            "message": "Remove unused import: `random`"
          },
          "location": {
            "column": 8,
            "row": 2
          },
          "message": "`random` imported but unused",
          "noqa_row": 2,
          "url": "https://docs.astral.sh/ruff/rules/unused-import",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 14,
            "row": 6
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import random\n\nfrom cocos.actions import CallFuncS, MoveTo\nfrom cocos.sprite import Sprite\n\nimport define\n\n\n",
                "end_location": {
                  "column": 1,
                  "row": 9
                },
                "location": {
                  "column": 1,
                  "row": 2
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 2
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 2,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 14,
            "row": 4
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import cocos\nfrom cocos.director import director\n\nimport define\n\n\n",
                "end_location": {
                  "column": 1,
                  "row": 6
                },
                "location": {
                  "column": 1,
                  "row": 2
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 2
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 2,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "B006",
          "end_location": {
            "column": 34,
            "row": 8
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gameover.py",
          "fix": {
            "applicability": "unsafe",
            "edits": [
              {
                "content": "None",
                "end_location": {
                  "column": 34,
                  "row": 8
                },
                "location": {
                  "column": 32,
                  "row": 8
                }
              },
              {
                "content": "        if banners is None:\n            banners = []\n",
                "end_location": {
                  "column": 1,
                  "row": 10
                },
                "location": {
                  "column": 1,
                  "row": 10
                }
              }
            ],
            "message": "Replace with `None`; initialize within function"
          },
          "location": {
            "column": 32,
            "row": 8
          },
          "message": "Do not use mutable data structures for argument defaults",
          "noqa_row": 8,
          "url": "https://docs.astral.sh/ruff/rules/mutable-argument-default",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 19,
            "row": 2
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import cocos.audio\n\n",
                "end_location": {
                  "column": 1,
                  "row": 3
                },
                "location": {
                  "column": 1,
                  "row": 2
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 2
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 2,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 13,
            "row": 6
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 6
          },
          "message": "Module level import not at top of file",
          "noqa_row": 6,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 30,
            "row": 12
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import cocos\nfrom cocos.director import director\nfrom cocos.scene import Scene\n\nimport define\nfrom arena import Arena\nfrom gameover import Gameover\n\n\n",
                "end_location": {
                  "column": 1,
                  "row": 14
                },
                "location": {
                  "column": 1,
                  "row": 6
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 6
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 6,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 36,
            "row": 7
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 7
          },
          "message": "Module level import not at top of file",
          "noqa_row": 7,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 30,
            "row": 8
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 8
          },
          "message": "Module level import not at top of file",
          "noqa_row": 8,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 14,
            "row": 10
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 10
          },
          "message": "Module level import not at top of file",
          "noqa_row": 10,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 24,
            "row": 11
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 11
          },
          "message": "Module level import not at top of file",
          "noqa_row": 11,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E402",
          "end_location": {
            "column": 30,
            "row": 12
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": null,
          "location": {
            "column": 1,
            "row": 12
          },
          "message": "Module level import not at top of file",
          "noqa_row": 12,
          "url": "https://docs.astral.sh/ruff/rules/module-import-not-at-top-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "W292",
          "end_location": {
            "column": 34,
            "row": 59
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "\n",
                "end_location": {
                  "column": 34,
                  "row": 59
                },
                "location": {
                  "column": 34,
                  "row": 59
                }
              }
            ],
            "message": "Add trailing newline"
          },
          "location": {
            "column": 34,
            "row": 59
          },
          "message": "No newline at end of file",
          "noqa_row": 59,
          "url": "https://docs.astral.sh/ruff/rules/missing-newline-at-end-of-file",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "I001",
          "end_location": {
            "column": 20,
            "row": 9
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "import math\nimport os  # Intentional: unused import to be flagged by linters\nimport random\n\nimport cocos\nfrom cocos.sprite import Sprite\n\nimport define\nfrom dot import Dot\n\n\n",
                "end_location": {
                  "column": 1,
                  "row": 12
                },
                "location": {
                  "column": 1,
                  "row": 2
                }
              }
            ],
            "message": "Organize imports"
          },
          "location": {
            "column": 1,
            "row": 2
          },
          "message": "Import block is un-sorted or un-formatted",
          "noqa_row": 2,
          "url": "https://docs.astral.sh/ruff/rules/unsorted-imports",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "F401",
          "end_location": {
            "column": 10,
            "row": 3
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": {
            "applicability": "safe",
            "edits": [
              {
                "content": "",
                "end_location": {
                  "column": 1,
                  "row": 4
                },
                "location": {
                  "column": 1,
                  "row": 3
                }
              }
            ],
            "message": "Remove unused import: `os`"
          },
          "location": {
            "column": 8,
            "row": 3
          },
          "message": "`os` imported but unused",
          "noqa_row": 3,
          "url": "https://docs.astral.sh/ruff/rules/unused-import",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "F841",
          "end_location": {
            "column": 13,
            "row": 68
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": {
            "applicability": "unsafe",
            "edits": [
              {
                "content": "",
                "end_location": {
                  "column": 1,
                  "row": 69
                },
                "location": {
                  "column": 1,
                  "row": 68
                }
              }
            ],
            "message": "Remove assignment to unused variable `list`"
          },
          "location": {
            "column": 9,
            "row": 68
          },
          "message": "Local variable `list` is assigned to but never used",
          "noqa_row": 68,
          "url": "https://docs.astral.sh/ruff/rules/unused-variable",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E722",
          "end_location": {
            "column": 15,
            "row": 77
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": null,
          "location": {
            "column": 9,
            "row": 77
          },
          "message": "Do not use bare `except`",
          "noqa_row": 77,
          "url": "https://docs.astral.sh/ruff/rules/bare-except",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "B007",
          "end_location": {
            "column": 14,
            "row": 84
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": {
            "applicability": "unsafe",
            "edits": [
              {
                "content": "_i",
                "end_location": {
                  "column": 14,
                  "row": 84
                },
                "location": {
                  "column": 13,
                  "row": 84
                }
              }
            ],
            "message": "Rename unused `i` to `_i`"
          },
          "location": {
            "column": 13,
            "row": 84
          },
          "message": "Loop control variable `i` not used within loop body",
          "noqa_row": 84,
          "url": "https://docs.astral.sh/ruff/rules/unused-loop-control-variable",
          "tool": "ruff"
        },
        {
          "cell": null,
          "code": "E741",
          "end_location": {
            "column": 10,
            "row": 144
          },
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "fix": null,
          "location": {
            "column": 9,
            "row": 144
          },
          "message": "Ambiguous variable name: `l`",
          "noqa_row": 144,
          "url": "https://docs.astral.sh/ruff/rules/ambiguous-variable-name",
          "tool": "ruff"
        },
        {
          "type": "warning",
          "module": "arena",
          "obj": "Arena.__init__",
          "line": 22,
          "column": 12,
          "endLine": 22,
          "endColumn": 13,
          "path": "arena.py",
          "symbol": "unused-variable",
          "message": "Unused variable 'i'",
          "message-id": "W0612",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "arena",
          "obj": "Arena.add_enemy",
          "line": 41,
          "column": 8,
          "endLine": 43,
          "endColumn": 16,
          "path": "arena.py",
          "symbol": "bare-except",
          "message": "No exception type(s) specified",
          "message-id": "W0702",
          "tool": "pylint"
        },
        {
          "type": "error",
          "module": "arena",
          "obj": "Arena.add_enemy",
          "line": 40,
          "column": 34,
          "endLine": 40,
          "endColumn": 61,
          "path": "arena.py",
          "symbol": "no-member",
          "message": "Instance of 'Snake' has no 'nonexistent_attribute' member",
          "message-id": "E1101",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "arena",
          "obj": "Arena.update",
          "line": 45,
          "column": 21,
          "endLine": 45,
          "endColumn": 23,
          "path": "arena.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'dt'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "arena",
          "obj": "Arena.on_key_press",
          "line": 49,
          "column": 32,
          "endLine": 49,
          "endColumn": 41,
          "path": "arena.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'modifiers'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "arena",
          "obj": "Arena.on_key_release",
          "line": 53,
          "column": 35,
          "endLine": 53,
          "endColumn": 44,
          "path": "arena.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'modifiers'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "define",
          "obj": "",
          "line": 2,
          "column": 0,
          "endLine": 2,
          "endColumn": 13,
          "path": "define.py",
          "symbol": "unused-import",
          "message": "Unused import random",
          "message-id": "W0611",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "dot",
          "obj": "Dot.__init__",
          "line": 35,
          "column": 15,
          "endLine": 35,
          "endColumn": 24,
          "path": "dot.py",
          "symbol": "broad-exception-caught",
          "message": "Catching too general exception Exception",
          "message-id": "W0718",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "dot",
          "obj": "Dot.update",
          "line": 49,
          "column": 21,
          "endLine": 49,
          "endColumn": 23,
          "path": "dot.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'dt'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "dot",
          "obj": "Dot.check_kill",
          "line": 61,
          "column": 12,
          "endLine": 61,
          "endColumn": 23,
          "path": "dot.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute 'killer' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gameover",
          "obj": "Gameover.__init__",
          "line": 8,
          "column": 4,
          "endLine": 8,
          "endColumn": 16,
          "path": "gameover.py",
          "symbol": "dangerous-default-value",
          "message": "Dangerous default value [] as argument",
          "message-id": "W0102",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "unsafe_eval",
          "line": 20,
          "column": 11,
          "endLine": 20,
          "endColumn": 20,
          "path": "gluttonous.py",
          "symbol": "broad-exception-caught",
          "message": "Catching too general exception Exception",
          "message-id": "W0718",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "unsafe_eval",
          "line": 19,
          "column": 19,
          "endLine": 19,
          "endColumn": 29,
          "path": "gluttonous.py",
          "symbol": "eval-used",
          "message": "Use of eval",
          "message-id": "W0123",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "HelloWorld.on_mouse_press",
          "line": 48,
          "column": 29,
          "endLine": 48,
          "endColumn": 30,
          "path": "gluttonous.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'x'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "HelloWorld.on_mouse_press",
          "line": 48,
          "column": 32,
          "endLine": 48,
          "endColumn": 33,
          "path": "gluttonous.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'y'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "HelloWorld.on_mouse_press",
          "line": 48,
          "column": 35,
          "endLine": 48,
          "endColumn": 42,
          "path": "gluttonous.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'buttons'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "gluttonous",
          "obj": "HelloWorld.on_mouse_press",
          "line": 48,
          "column": 44,
          "endLine": 48,
          "endColumn": 53,
          "path": "gluttonous.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'modifiers'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_body",
          "line": 68,
          "column": 8,
          "endLine": 68,
          "endColumn": 12,
          "path": "snake.py",
          "symbol": "redefined-builtin",
          "message": "Redefining built-in 'list'",
          "message-id": "W0622",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_body",
          "line": 65,
          "column": 15,
          "endLine": 65,
          "endColumn": 24,
          "path": "snake.py",
          "symbol": "broad-exception-caught",
          "message": "Catching too general exception Exception",
          "message-id": "W0718",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_body",
          "line": 77,
          "column": 8,
          "endLine": 78,
          "endColumn": 53,
          "path": "snake.py",
          "symbol": "bare-except",
          "message": "No exception type(s) specified",
          "message-id": "W0702",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_body",
          "line": 68,
          "column": 8,
          "endLine": 68,
          "endColumn": 12,
          "path": "snake.py",
          "symbol": "unused-variable",
          "message": "Unused variable 'list'",
          "message-id": "W0612",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.init_body",
          "line": 84,
          "column": 12,
          "endLine": 84,
          "endColumn": 13,
          "path": "snake.py",
          "symbol": "unused-variable",
          "message": "Unused variable 'i'",
          "message-id": "W0612",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.ai",
          "line": 149,
          "column": 17,
          "endLine": 149,
          "endColumn": 19,
          "path": "snake.py",
          "symbol": "unused-argument",
          "message": "Unused argument 'dt'",
          "message-id": "W0613",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_body",
          "line": 63,
          "column": 16,
          "endLine": 63,
          "endColumn": 31,
          "path": "snake.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute '_tmp_store' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.init_body",
          "line": 81,
          "column": 8,
          "endLine": 81,
          "endColumn": 18,
          "path": "snake.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute 'score' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.init_body",
          "line": 82,
          "column": 8,
          "endLine": 82,
          "endColumn": 19,
          "path": "snake.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute 'length' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.add_score",
          "line": 146,
          "column": 12,
          "endLine": 146,
          "endColumn": 23,
          "path": "snake.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute 'length' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "Snake.init_body",
          "line": 83,
          "column": 8,
          "endLine": 83,
          "endColumn": 17,
          "path": "snake.py",
          "symbol": "attribute-defined-outside-init",
          "message": "Attribute 'body' defined outside __init__",
          "message-id": "W0201",
          "tool": "pylint"
        },
        {
          "type": "warning",
          "module": "snake",
          "obj": "",
          "line": 3,
          "column": 0,
          "endLine": 3,
          "endColumn": 9,
          "path": "snake.py",
          "symbol": "unused-import",
          "message": "Unused import os",
          "message-id": "W0611",
          "tool": "pylint"
        },
        {
          "code": "40             enemy.optional_attr = enemy.nonexistent_attribute\n41         except:\n42             # swallow everything deliberately\n43             pass\n44 \n",
          "col_offset": 8,
          "end_col_offset": 16,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\arena.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 703,
            "link": "https://cwe.mitre.org/data/definitions/703.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Try, Except, Pass detected.",
          "line_number": 41,
          "line_range": [
            41,
            42,
            43
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
          "test_id": "B110",
          "test_name": "try_except_pass",
          "tool": "bandit"
        },
        {
          "code": "24         if color is None:\n25             color = random.choice(define.ALL_COLOR)\n26 \n",
          "col_offset": 20,
          "end_col_offset": 51,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 25,
          "line_range": [
            25
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "34             # no f.close() here — deliberate\n35         except Exception:\n36             # ignore file errors intentionally\n37             pass\n38         if pos is None:\n",
          "col_offset": 8,
          "end_col_offset": 16,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 703,
            "link": "https://cwe.mitre.org/data/definitions/703.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Try, Except, Pass detected.",
          "line_number": 35,
          "line_range": [
            35,
            36,
            37
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
          "test_id": "B110",
          "test_name": "try_except_pass",
          "tool": "bandit"
        },
        {
          "code": "38         if pos is None:\n39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n",
          "col_offset": 29,
          "end_col_offset": 66,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 39,
          "line_range": [
            39
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "39             self.position = (random.randint(40, define.WIDTH - 40),\n40                              random.randint(40, define.HEIGHT - 40))\n41             self.is_big = False\n",
          "col_offset": 29,
          "end_col_offset": 67,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 40,
          "line_range": [
            40
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "43         else:\n44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n",
          "col_offset": 38,
          "end_col_offset": 53,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 44,
          "line_range": [
            44
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "44             self.position = (pos[0] + random.random() * 32 - 16,\n45                              pos[1] + random.random() * 32 - 16)\n46             self.is_big = True\n",
          "col_offset": 38,
          "end_col_offset": 53,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 45,
          "line_range": [
            45
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "46             self.is_big = True\n47         self.schedule_interval(self.update, random.random() * 0.2 + 0.1)\n48 \n",
          "col_offset": 44,
          "end_col_offset": 59,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\dot.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 47,
          "line_range": [
            47
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "18         if isinstance(expr, str) and len(expr) < 50:\n19             return eval(expr)\n20     except Exception:\n",
          "col_offset": 19,
          "end_col_offset": 29,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\gluttonous.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 78,
            "link": "https://cwe.mitre.org/data/definitions/78.html"
          },
          "issue_severity": "MEDIUM",
          "issue_text": "Use of possibly insecure function - consider using safer ast.literal_eval.",
          "line_number": 19,
          "line_range": [
            19
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b307-eval",
          "test_id": "B307",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "17         self.is_dead = False\n18         self.angle = random.randrange(360)  # 目前角度\n19         self.angle_dest = self.angle  # 目标角度\n",
          "col_offset": 21,
          "end_col_offset": 42,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 18,
          "line_range": [
            18
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "19         self.angle_dest = self.angle  # 目标角度\n20         self.color = random.choice(define.ALL_COLOR)\n21         self.no = Snake.no\n",
          "col_offset": 21,
          "end_col_offset": 52,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 20,
          "line_range": [
            20
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
          "col_offset": 28,
          "end_col_offset": 55,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 24,
          "line_range": [
            24
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "23         if is_enemy:\n24             self.position = random.randrange(300, 1300), random.randrange(200, 600)\n25             if 600 < self.x < 1000:\n",
          "col_offset": 57,
          "end_col_offset": 83,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 24,
          "line_range": [
            24
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
          "col_offset": 28,
          "end_col_offset": 54,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 28,
          "line_range": [
            28
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "27         else:\n28             self.position = random.randrange(700, 900), random.randrange(350, 450)\n29         self.is_enemy = is_enemy\n",
          "col_offset": 56,
          "end_col_offset": 82,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 28,
          "line_range": [
            28
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "55         if self.is_enemy:\n56             self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)\n57 \n",
          "col_offset": 44,
          "end_col_offset": 59,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 56,
          "line_range": [
            56
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        },
        {
          "code": "64             self._tmp_store.append(self.color)\n65         except Exception:\n66             pass\n67         # Intentional: shadow built-in name to create a detectable smell\n",
          "col_offset": 8,
          "end_col_offset": 16,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 703,
            "link": "https://cwe.mitre.org/data/definitions/703.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Try, Except, Pass detected.",
          "line_number": 65,
          "line_range": [
            65,
            66
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/plugins/b110_try_except_pass.html",
          "test_id": "B110",
          "test_name": "try_except_pass",
          "tool": "bandit"
        },
        {
          "code": "185             if abs(angle - self.angle_dest) < 5:\n186                 self.angle_dest += random.randrange(90, 270)\n187 \n",
          "col_offset": 35,
          "end_col_offset": 60,
          "filename": "C:\\Users\\lenovo\\AppData\\Local\\Temp\\scan_19ttvsqd\\snake.py",
          "issue_confidence": "HIGH",
          "issue_cwe": {
            "id": 330,
            "link": "https://cwe.mitre.org/data/definitions/330.html"
          },
          "issue_severity": "LOW",
          "issue_text": "Standard pseudo-random generators are not suitable for security/cryptographic purposes.",
          "line_number": 186,
          "line_range": [
            186
          ],
          "more_info": "https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b311-random",
          "test_id": "B311",
          "test_name": "blacklist",
          "tool": "bandit"
        }
      ],
      "dynamic_results": {
        "py_compile": [],
        "pytest": {
          "skipped": true,
          "reason": "未配置测试"
        },
        "dynamic_detection": {
          "enabled": true,
          "categories": {
            "user_input": [],
            "resource_management": [
              {
                "file": "dot.py",
                "line": 32,
                "col": 16,
                "category": "resource_management",
                "severity": "HIGH",
                "rule_id": "DYN-RES-001",
                "message": "文件打开未使用 with 语句，可能导致资源泄漏",
                "snippet": "            f = open('getqrcode.jpeg', 'rb')",
                "suggestion": "使用 with open(...) as f: 确保文件自动关闭"
              }
            ],
            "concurrency": [],
            "boundary_conditions": [
              {
                "file": "arena.py",
                "line": 13,
                "col": 23,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "arena.py",
                "line": 13,
                "col": 58,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "gameover.py",
                "line": 12,
                "col": 25,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.position = (director.get_window_size()[0] / 2 - 200,",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "gameover.py",
                "line": 13,
                "col": 25,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                         director.get_window_size()[1] / 2 - 150)",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 109,
                "col": 27,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 110,
                "col": 27,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 113,
                "col": 24,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        lag = int(round(1100.0 / self.speed))",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 114,
                "col": 8,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-001",
                "message": "循环中的数组访问可能越界",
                "snippet": "        for i in range(len(self.body)):",
                "suggestion": "确保索引在有效范围内，考虑使用 enumerate()"
              },
              {
                "file": "snake.py",
                "line": 144,
                "col": 12,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "        l = (self.score - 6) / 6",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 181,
                "col": 24,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                angle = math.atan(d_y / d_x) * 180 / math.pi",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 181,
                "col": 34,
                "category": "boundary_conditions",
                "severity": "MEDIUM",
                "rule_id": "DYN-BOUND-002",
                "message": "除法操作可能导致除零错误",
                "snippet": "                angle = math.atan(d_y / d_x) * 180 / math.pi",
                "suggestion": "检查除数是否为零"
              },
              {
                "file": "snake.py",
                "line": 197,
                "col": 28,
                "category": "boundary_conditions",
                "severity": "LOW",
                "rule_id": "DYN-BOUND-003",
                "message": "幂运算可能导致溢出",
                "snippet": "            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)",
                "suggestion": "检查输入范围，防止数值溢出"
              },
              {
                "file": "snake.py",
                "line": 197,
                "col": 50,
                "category": "boundary_conditions",
                "severity": "LOW",
                "rule_id": "DYN-BOUND-003",
                "message": "幂运算可能导致溢出",
                "snippet": "            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)",
                "suggestion": "检查输入范围，防止数值溢出"
              }
            ],
            "environment_config": [],
            "dynamic_execution": [
              {
                "file": "gluttonous.py",
                "line": 19,
                "col": 19,
                "category": "dynamic_execution",
                "severity": "HIGH",
                "rule_id": "DYN-EXEC-001",
                "message": "使用 eval() 存在代码注入风险",
                "snippet": "            return eval(expr)",
                "suggestion": "避免使用 eval/exec，或严格验证输入"
              }
            ]
          },
          "summary": {
            "total": 15,
            "by_category": {
              "resource_management": 1,
              "boundary_conditions": 13,
              "dynamic_execution": 1
            },
            "by_severity": {
              "HIGH": 2,
              "MEDIUM": 11,
              "LOW": 2
            }
          }
        }
      }
    }
  ]
}
```
