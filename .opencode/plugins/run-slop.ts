import { spawn } from "node:child_process"
import { isAbsolute, resolve } from "node:path"

import { Plugin } from "@opencode/plugin"

interface RunResult {
  stdout: string
  stderr: string
  exitCode: number | null
}

function runSlop(root: string, file: string): Promise<RunResult> {
  return new Promise((resolvePromise, reject) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd: root,
      stdio: ["ignore", "pipe", "pipe"],
    })

    const stdout: Buffer[] = []
    const stderr: Buffer[] = []

    child.stdout.on("data", (chunk: Buffer) => stdout.push(chunk))
    child.stderr.on("data", (chunk: Buffer) => stderr.push(chunk))
    child.on("error", (error) => reject(error))
    child.on("close", (exitCode) => {
      resolvePromise({
        stdout: Buffer.concat(stdout).toString("utf8"),
        stderr: Buffer.concat(stderr).toString("utf8"),
        exitCode,
      })
    })
  })
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    const root = ctx.location.project.canonical

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description: "Run a SlopLang file with Sloperator and return stdout, stderr, and exitCode.",
        input: {
          type: "object",
          properties: {
            path: { type: "string", description: "Path to the .slop file, relative to the project root." },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string }
          const file = isAbsolute(path) ? path : resolve(root, path)
          const result = await runSlop(root, file)
          return { content: JSON.stringify(result) }
        },
      })
    })
  },
})
