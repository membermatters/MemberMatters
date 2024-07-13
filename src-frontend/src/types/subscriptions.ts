import { z } from 'zod';

export const SubscriptionStateSchema = z.enum([
  'inactive',
  'active',
  'cancelling',
]);
export type SubscriptionState = z.infer<typeof SubscriptionStateSchema>;

export const MemberPlanSchema = z.object({
  id: z.number(),
  name: z.string(),
  currency: z.string(),
  cost: z.number(),
  intervalAmount: z.number(),
  interval: z.string(),
});

export type MemberPlan = z.infer<typeof MemberPlanSchema>;

export const MemberTierSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string(),
  featured: z.boolean(),
  plans: z.array(MemberPlanSchema),
});

export type MemberTier = z.infer<typeof MemberTierSchema>;

export const MemberSubscriptionSchema = z.object({
  billingCycleAnchor: z.date(),
  cancelAt: z.date(),
  cancelAtPeriodEnd: z.boolean(),
  currentPeriodEnd: z.date(),
  startDate: z.date(),
  status: z.string(),
  membershipPlan: MemberPlanSchema,
  membershipTier: MemberTierSchema,
});

export type MemberSubscription = z.infer<typeof MemberSubscriptionSchema>;
