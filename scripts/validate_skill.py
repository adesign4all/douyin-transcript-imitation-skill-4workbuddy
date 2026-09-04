#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_skill.py - 校验 SKILL.md 的 frontmatter 与目录完整性

用法:
    python scripts/validate_skill.py SKILL.md
    python scripts/validate_skill.py SKILL.md --strict
    python scripts/validate_skill.py SKILL.md --repo-root .

退出码:
    0 - 全部通过
    1 - 校验失败
    2 - 文件不存在
"""
import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: 需要安装 pyyaml, 运行: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# WorkBuddy 开放平台要求的必填 frontmatter 字段
REQUIRED_FIELDS = {
    "name": str,
    "display_name": str,
    "description": str,
    "version": str,
    "category": str,
    "author": str,
}

# 强烈推荐字段（缺会警告但不会失败）
RECOMMENDED_FIELDS = {
    "display_name_en": str,
    "description_zh": str,
    "description_en": str,
    "allowed-tools": str,
}

# 占位符（上传前必须替换）
PLACEHOLDER_VALUES = {
    "WorkBuddy User",
    "user@workbuddy.cn",
    "your-username",
    "your-feature",
    "TODO",
    "FIXME",
    "XXX",
}


def extract_frontmatter(text: str) -> tuple:
    """提取 SKILL.md 的 YAML frontmatter。返回 (frontmatter_dict, error_message)"""
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    match = pattern.match(text)
    if not match:
        return None, "ERROR: 找不到 YAML frontmatter（需要 --- 包裹的开头）"
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return None, f"ERROR: YAML 解析失败: {e}"
    if not isinstance(fm, dict):
        return None, f"ERROR: frontmatter 不是 dict 类型, 实际是 {type(fm).__name__}"
    return fm, None


def validate_required(fm: dict) -> list:
    """校验必填字段"""
    errors = []
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in fm:
            errors.append(f"ERROR: 缺少必填字段: {field}")
        elif not isinstance(fm[field], expected_type):
            errors.append(
                f"ERROR: 字段 {field} 类型错误: "
                f"期望 {expected_type.__name__}, 实际 {type(fm[field]).__name__}"
            )
        elif not str(fm[field]).strip():
            errors.append(f"ERROR: 字段 {field} 不能为空")
    return errors


def validate_recommended(fm: dict) -> list:
    """校验推荐字段（仅警告）"""
    warnings = []
    for field, expected_type in RECOMMENDED_FIELDS.items():
        if field not in fm:
            warnings.append(f"WARN: 建议补充字段: {field}")
    return warnings


def validate_placeholders(fm: dict) -> list:
    """检查是否还有占位符未替换"""
    warnings = []
    for key, val in fm.items():
        if not isinstance(val, str):
            continue
        for ph in PLACEHOLDER_VALUES:
            if ph.lower() in val.lower():
                warnings.append(f"WARN: 字段 {key} 含占位符 '{ph}', 上传前请替换")
    return warnings


def validate_version(fm: dict) -> list:
    """校验版本号格式 (semver)"""
    errors = []
    ver = fm.get("version", "")
    if ver and not re.match(r"^\d+\.\d+\.\d+", str(ver)):
        errors.append(f"ERROR: version 字段应为 semver 格式 (如 1.0.0), 实际: {ver}")
    return errors


def validate_repo_structure(repo_root: Path, fm: dict) -> list:
    """校验仓库结构完整性"""
    errors = []
    warnings = []

    required_files = ["SKILL.md", "README.md", "LICENSE", "CHANGELOG.md"]
    for f in required_files:
        if not (repo_root / f).exists():
            errors.append(f"ERROR: 缺少文件: {f}")

    required_dirs = ["references", "templates", "scripts"]
    for d in required_dirs:
        if not (repo_root / d).is_dir():
            errors.append(f"ERROR: 缺少目录: {d}/")
        elif not list((repo_root / d).iterdir()):
            warnings.append(f"WARN: 目录为空: {d}/")

    # 校验 templates 应有 3 个标准模板
    templates = list((repo_root / "templates").glob("*.md")) if (repo_root / "templates").is_dir() else []
    expected_templates = {"transcript-template.md", "analysis-template.md", "imitation-template.md"}
    actual_templates = {t.name for t in templates}
    missing = expected_templates - actual_templates
    if missing:
        warnings.append(f"WARN: 缺少标准模板: {missing}")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="校验 SKILL.md 的 frontmatter 与仓库结构"
    )
    parser.add_argument("skill_path", help="SKILL.md 路径")
    parser.add_argument("--repo-root", default=".", help="仓库根目录（默认当前目录）")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式，把 WARN 当作 ERROR",
    )
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    repo_root = Path(args.repo_root).resolve()

    if not skill_path.exists():
        print(f"ERROR: 文件不存在: {skill_path}", file=sys.stderr)
        sys.exit(2)

    print(f"📋 校验文件: {skill_path}")
    print(f"📁 仓库根目录: {repo_root}")
    print()

    # 读取并解析 frontmatter
    text = skill_path.read_text(encoding="utf-8")
    fm, err = extract_frontmatter(text)
    if err:
        print(err)
        sys.exit(1)
    print(f"✓ YAML frontmatter 解析成功（{len(fm)} 个字段）")

    # 字段名展示
    print("  字段清单:")
    for k, v in fm.items():
        v_disp = (v[:50] + "...") if isinstance(v, str) and len(v) > 50 else v
        print(f"    {k:20s} = {v_disp!r}")
    print()

    # 校验
    all_errors = []
    all_warnings = []

    all_errors.extend(validate_required(fm))
    all_warnings.extend(validate_recommended(fm))
    all_warnings.extend(validate_placeholders(fm))
    all_errors.extend(validate_version(fm))

    errs, warns = validate_repo_structure(repo_root, fm)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 输出
    if all_warnings:
        print("⚠️  警告:")
        for w in all_warnings:
            print(f"  {w}")
        print()

    if all_errors:
        print("❌ 错误:")
        for e in all_errors:
            print(f"  {e}")
        print()
        print(f"FAILED: {len(all_errors)} 个错误, {len(all_warnings)} 个警告")
        sys.exit(1)

    if args.strict and all_warnings:
        print(f"FAILED (strict): {len(all_warnings)} 个警告必须修复")
        sys.exit(1)

    print(f"✅ PASSED: {len(all_warnings)} 个警告, 0 个错误")
    sys.exit(0)


if __name__ == "__main__":
    main()
