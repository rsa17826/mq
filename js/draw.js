const activeContexts = new WeakMap()

function draw(ctx) {
  // 1. Restore baseline context state if a previous draw() modified it
  if (activeContexts.has(ctx)) {
    ctx.restore()
    activeContexts.delete(ctx)
  }

  // 2. Save current state for this drawing session
  ctx.save()
  const sessionToken = Symbol("drawSession")
  activeContexts.set(ctx, sessionToken)

  // 3. Cleanup microtask to restore state automatically after synchronous execution
  queueMicrotask(() => {
    if (activeContexts.get(ctx) === sessionToken) {
      ctx.restore()
      activeContexts.delete(ctx)
    }
  })

  // 4. Return Proxy to allow fluent method chaining
  const proxy = new Proxy(ctx, {
    get(target, prop) {
      // Sync strokeStyle and fillStyle so fillRect and strokeRect share colors
      if (prop === "strokeStyle" || prop === "fillStyle") {
        return function (color) {
          target.strokeStyle = color
          target.fillStyle = color
          return proxy
        }
      }

      const original = target[prop]

      // Handle native methods (e.g. fillRect, strokeRect, arc)
      if (typeof original === "function") {
        return function (...args) {
          original.apply(target, args)
          return proxy
        }
      }

      // Convert properties (e.g. lineJoin, lineWidth) into chainable setters
      return function (...args) {
        if (args.length > 0) {
          target[prop] = args[0]
          return proxy
        }
        return target[prop]
      }
    },
  })

  return proxy
}
