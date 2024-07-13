import { z } from 'zod';
import { MemberStateSchema } from 'types/member';
import { SubscriptionStateSchema } from 'types/subscriptions';
import { MemberbucksTransactionsTypeSchema } from 'types/memberbucks';

export const OnSiteMetricsSchema = z.object({
  members: z.array(z.string()),
  count: z.number(),
});

export type OnSiteMetrics = z.infer<typeof OnSiteMetricsSchema>;

export const MemberCountTotalSchema = z.object({
  date: z.string(),
  data: z.array(z.object({ state: MemberStateSchema, total: z.number() })),
});

export type MemberCountTotal = z.infer<typeof MemberCountTotalSchema>;

export const SubscriptionCountTotalSchema = z.object({
  date: z.string(),
  data: z.array(
    z.object({ state: SubscriptionStateSchema, total: z.number() })
  ),
});

export type SubscriptionCountTotal = z.infer<
  typeof SubscriptionCountTotalSchema
>;

export const MemberbucksBalanceTotalSchema = z.object({
  date: z.string(),
  data: z.object({ value: z.number() }),
});

export type MemberbucksBalanceTotal = z.infer<
  typeof MemberbucksBalanceTotalSchema
>;

export const MemberbucksTransactionsTotalSchema = z.object({
  date: z.string(),
  data: z.array(
    z.object({ type: MemberbucksTransactionsTypeSchema, total: z.number() })
  ),
});

export type MemberbucksTransactionsTotal = z.infer<
  typeof MemberbucksTransactionsTotalSchema
>;
